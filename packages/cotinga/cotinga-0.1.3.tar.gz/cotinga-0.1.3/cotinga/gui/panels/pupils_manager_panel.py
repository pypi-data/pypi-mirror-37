# -*- coding: utf-8 -*-

# Cotinga helps maths teachers creating worksheets
# and managing pupils' progression.
# Copyright 2018 Nicolas Hainaux <nh.techn@gmail.com>

# This file is part of Cotinga.

# Cotinga is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.

# Cotinga is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Cotinga; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import time
from gettext import translation

import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')
    gi.require_version('Pango', '1.0')
except ValueError:
    raise
else:
    from gi.repository import GLib, Gdk, Gtk, GObject, Pango


from cotinga.core.env import LOCALEDIR, L10N_DOMAIN
from cotinga.core.env import ICON_THEME, get_icon_theme_name, get_theme_colors
from cotinga.core.env import convert_gdk_rgba_to_hex
from cotinga.core.tools import Listing, cellfont_fmt, calculate_attained_level
from cotinga.core.tools import build_view
from cotinga.core import shared
from cotinga.models import Pupils, PUPILS_COL_NBS
from cotinga.gui.panels import ListManagerBase
from cotinga.gui.dialogs import ComboDialog, run_message_dialog
from cotinga.gui.dialogs import ConfirmationDialog
from cotinga import gui
from cotinga.core import constants
from cotinga.core.errors import EmptyContentError, ReservedCharsError

STEPS = constants.NUMERIC_STEPS
SEP = constants.INTERNAL_SEPARATOR

# Column numbers of the store
ID, INCLUDED, CLASS, FULLNAME, ILEVEL, ALEVEL, GRADES = (0, 1, 2, 3, 4, 5, 6)


class PupilsManagerPanel(ListManagerBase):

    def __init__(self, classname):
        # TODO: change mouse cursor when hovering editable columns
        self.classname = classname
        ListManagerBase.__init__(self, setup_buttons_icons=False,
                                 mini_items_nb=0,
                                 store_types=[str, bool, str, str, str, str,
                                              GObject.TYPE_PYOBJECT])
        PREFS = shared.PREFS
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext

        for pupil in shared.session.query(Pupils)\
                .filter_by(classname=classname):
            self.store.append([str(pupil.id), pupil.included, pupil.classname,
                               pupil.fullname, pupil.initial_level,
                               pupil.attained_level, Listing(pupil.grades)])

        self.store.set_sort_column_id(FULLNAME, Gtk.SortType.ASCENDING)

        liststore_levels = Gtk.ListStore(str)
        for item in self.levels:
            liststore_levels.append([item])

        def _set_cell_fgcolor(column, cell, model, it, ignored):
            """Turn not included pupils in grey."""
            included = model.get_value(it, INCLUDED)
            if included:
                fgcolor, _, _, _ = get_theme_colors()
                cell.set_property('foreground_rgba', fgcolor)
            else:
                cell.set_property('foreground', 'Grey')

        self.renderer_id = Gtk.CellRendererText()
        self.col_id = Gtk.TreeViewColumn('id', self.renderer_id, text=0)
        self.col_id.set_cell_data_func(self.renderer_id, _set_cell_fgcolor, '')
        self.col_id.set_visible(shared.STATUS.show_col_id)

        self.renderer_incl = Gtk.CellRendererToggle()
        self.renderer_incl.connect('toggled', self.on_included_toggled)
        self.col_incl = Gtk.TreeViewColumn(tr('Included'), self.renderer_incl,
                                           active=1)
        self.col_incl.set_visible(shared.STATUS.show_col_incl)

        self.renderer_class = Gtk.CellRendererText()
        col_class = Gtk.TreeViewColumn(tr('Class'), self.renderer_class,
                                       text=2)
        col_class.set_visible(False)

        self.renderer_name = Gtk.CellRendererText()
        self.renderer_name.props.editable = True
        self.renderer_name.props.editable_set = True
        self.renderer_name.connect('editing-started', self.on_editing_started)
        self.renderer_name.connect('editing_canceled',
                                   self.on_editing_canceled)
        self.renderer_name.connect('edited', self.on_name_edited)
        col_name = Gtk.TreeViewColumn(tr('Name'), self.renderer_name, text=3)
        col_name.set_cell_data_func(self.renderer_name, _set_cell_fgcolor, '')
        # col_name.set_sort_column_id(2)

        self.renderer_ilevel = Gtk.CellRendererCombo()
        self.renderer_ilevel.set_property('editable', True)
        self.renderer_ilevel.set_property('model', liststore_levels)
        self.renderer_ilevel.set_property('text-column', 0)
        self.renderer_ilevel.set_property('has-entry', False)
        self.renderer_ilevel.connect('editing-started',
                                     self.on_editing_started)
        self.renderer_ilevel.connect('edited', self.on_initial_level_edited)
        self.renderer_ilevel.connect('editing_canceled',
                                     self.on_editing_canceled)
        self.col_ilevel = Gtk.TreeViewColumn(tr('Initial level'),
                                             self.renderer_ilevel, text=4)
        self.col_ilevel.set_cell_data_func(self.renderer_ilevel,
                                           _set_cell_fgcolor, '')
        self.col_ilevel.set_visible(shared.STATUS.show_col_ilevel)
        # self.col_ilevel.set_sort_column_id(3)

        self.renderer_alevel = Gtk.CellRendererText()
        col_alevel = Gtk.TreeViewColumn(tr('Attained level'),
                                        self.renderer_alevel, text=5)
        col_alevel.set_cell_data_func(self.renderer_alevel,
                                      _set_cell_fgcolor, '')
        # col_alevel.set_sort_column_id(4)

        for i, col in enumerate([self.col_id, self.col_incl, col_class,
                                 col_name, self.col_ilevel, col_alevel]):
            # TODO: do not set a minimum width (or not hardcoded at least)
            # instead, check properties of Gtk.TreeViewColumn objects and see
            # what's possible
            # col.set_min_width(100)
            self.treeview.append_column(col)

        # LATER: factorize following common code between pupils manager and
        # view panels (add an intermediate class between ListManagerBase and
        # Pupil*Panel, that will have the common code)
        if self.grading['choice'] == 'numeric':
            self.grades_cell_width = \
                len(str(self.grading['maximum'])) \
                + len(STEPS[self.grading['step']]) - 1
        else:  # self.grading['choice'] == 'literal'
            self.grades_cell_width = \
                max([len(item) for item in self.grading['literal_grades']])
        max_special_grades = max([len(item) for item in self.special_grades])
        # 3 is the default minimal value in Gtk (could be omitted here)
        self.grades_cell_width = max(3, max_special_grades + 1,
                                     self.grades_cell_width + 1)

        for i in range(self.grades_nb):
            self.__add_grade_col(i)

        empty_right_grid = Gtk.Grid()
        empty_right_grid.set_hexpand(True)
        scrolled_grid = Gtk.Grid()
        scrolled_grid.attach(self.treeview, 0, 0, 1, 1)
        scrolled_grid.attach_next_to(empty_right_grid, self.treeview,
                                     Gtk.PositionType.RIGHT, 1, 1)

        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.add(scrolled_grid)
        self.scrollable_treelist.set_vexpand(True)
        self.attach(self.scrollable_treelist, 0, 0, 15, 10)

        # RIGHT TOOLS (add a grade...)
        self.right_tools = Gtk.Grid()
        self.right_tools.set_vexpand(False)

        self.add_grade_button = Gtk.ToolButton.new()
        self.add_grade_button.set_vexpand(False)
        self.add_grade_button.set_margin_bottom(5)
        self.add_grade_button.connect('clicked', self.on_add_grade_clicked)

        self.paste_grades_button = Gtk.ToolButton.new()
        self.paste_grades_button.set_vexpand(False)
        self.paste_grades_button.connect('clicked',
                                         self.on_paste_grades_clicked)

        self.paste_grades_button.set_sensitive(len(self.store) >= 1)
        self.add_grade_button.set_sensitive(len(self.store) >= 1)

        self.right_tools.attach(self.add_grade_button, 0, 0, 1, 1)
        self.right_tools.attach_next_to(self.paste_grades_button,
                                        self.add_grade_button,
                                        Gtk.PositionType.BOTTOM, 1, 1)

        self.attach_next_to(self.right_tools, self.scrollable_treelist,
                            Gtk.PositionType.RIGHT, 1, 1)

        # BOTTOM TOOLS (add/remove pupil)
        self.bottom_buttons = Gtk.Grid()

        self.insert_button.set_vexpand(False)
        self.insert_button.set_halign(Gtk.Align.CENTER)
        self.insert_button.set_valign(Gtk.Align.CENTER)
        self.insert_button.props.margin_right = 10
        self.insert_button.connect('clicked', self.on_insert_clicked)
        self.bottom_buttons.attach(self.insert_button, 0, 0, 1, 1)

        self.paste_pupils_button = Gtk.ToolButton.new()
        self.paste_pupils_button.set_vexpand(False)
        self.paste_pupils_button.set_hexpand(False)
        self.paste_pupils_button.set_halign(Gtk.Align.CENTER)
        self.paste_pupils_button.set_valign(Gtk.Align.CENTER)
        self.paste_pupils_button.props.margin_right = 10
        self.paste_pupils_button.connect('clicked',
                                         self.on_paste_pupils_clicked)
        self.bottom_buttons.attach_next_to(self.paste_pupils_button,
                                           self.insert_button,
                                           Gtk.PositionType.RIGHT, 1, 1)

        self.remove_button.set_vexpand(False)
        self.remove_button.set_halign(Gtk.Align.CENTER)
        self.remove_button.set_valign(Gtk.Align.CENTER)
        self.remove_button.set_sensitive(False)
        self.remove_button.connect('clicked', self.on_remove_clicked)
        self.bottom_buttons.attach_next_to(self.remove_button,
                                           self.paste_pupils_button,
                                           Gtk.PositionType.RIGHT, 1, 1)

        self.edit_level_button = Gtk.ToolButton.new()
        self.edit_level_button.set_vexpand(False)
        self.edit_level_button.set_hexpand(False)
        self.edit_level_button.set_halign(Gtk.Align.CENTER)
        self.edit_level_button.set_valign(Gtk.Align.CENTER)
        self.edit_level_button.props.margin_right = 10
        self.edit_level_button.set_sensitive(False)
        self.edit_level_button.connect('clicked',
                                       self.on_edit_level_clicked)
        self.bottom_buttons.attach_next_to(self.edit_level_button,
                                           self.remove_button,
                                           Gtk.PositionType.RIGHT, 1, 1)

        self.edit_class_button = Gtk.ToolButton.new()
        self.edit_class_button.set_vexpand(False)
        self.edit_class_button.set_hexpand(False)
        self.edit_class_button.set_halign(Gtk.Align.CENTER)
        self.edit_class_button.set_valign(Gtk.Align.CENTER)
        self.edit_class_button.props.margin_right = 10
        self.edit_class_button.set_sensitive(False)
        self.edit_class_button.connect('clicked',
                                       self.on_edit_class_clicked)
        self.bottom_buttons.attach_next_to(self.edit_class_button,
                                           self.edit_level_button,
                                           Gtk.PositionType.RIGHT, 1, 1)

        self.bottom_tools = Gtk.Grid()
        self.bottom_tools.set_hexpand(False)
        self.bottom_tools.props.margin_bottom = 0
        self.bottom_tools.props.margin_top = 3
        self.bottom_tools.attach(self.bottom_buttons, 0, 0, 1, 1)

        self.attach_next_to(self.bottom_tools, self.scrollable_treelist,
                            Gtk.PositionType.BOTTOM, 1, 1)

        bottomvoid_grid = Gtk.Grid()
        bottomvoid_grid.set_hexpand(True)
        self.attach_next_to(bottomvoid_grid, self.bottom_tools,
                            Gtk.PositionType.RIGHT, 1, 1)

        self.clip = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
        self.clip2 = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        # self.treeview.connect('set-focus-child', self.on_set_focus_child)
        self.started_edition = False
        self.setup_buttons_icons(ICON_THEME)

        # Only colgrades can be user selected
        self.user_selected_col = None
        self.unselected_rows = None

    @property
    def default_row_values(self):
        return [None, True, self.classname, None, self.levels[0],
                self.levels[0], Listing(None)]

    @property
    def grades_nb(self):
        class_pupils = shared.session.query(Pupils)\
            .filter_by(classname=self.classname)\
            .all()
        return max([len(pupil.grades or []) for pupil in class_pupils] or [0])

    def buttons_icons(self):
        # Last item of each list is the fallback, hence must be standard
        buttons = {'insert_button': ['contact-new'],
                   'remove_button': ['list-remove-user', 'edit-delete'],
                   'edit_level_button': ['starred'],
                   'edit_class_button': ['go-next'],
                   'paste_pupils_button': ['user-group-new',
                                           'stock_new-meeting',
                                           'resource-group-new',
                                           'stock_people', 'edit-paste'],
                   'paste_grades_button': ['edit-paste'],
                   'add_grade_button': ['list-add']}
        if any(get_icon_theme_name().startswith(name)
               for name in ['Numix-Circle', 'Paper']):
            buttons.update({'paste_grades_button': ['view-task', 'stock_task',
                                                    'edit-paste']})
        return buttons

    def buttons_labels(self):
        """Define labels of buttons."""
        PREFS = shared.PREFS
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
        buttons = {'insert_button': tr('Insert a pupil'),
                   'remove_button': tr('Remove pupils'),
                   'edit_level_button': tr('Edit initial level'),
                   'edit_class_button': tr('Edit class'),
                   'paste_pupils_button': tr('Paste pupils'),
                   'paste_grades_button': tr('Paste grades'),
                   'add_grade_button': tr('Add new grade')}
        return buttons

    def set_buttons_sensitivity(self):
        ListManagerBase.set_buttons_sensitivity(self)
        editing = self.started_insertion or self.started_edition
        rows_nb = len(self.selection.get_selected_rows()[1])
        lock_grades_btns = True
        colgrades_nb = self.treeview.get_n_columns() - GRADES
        no_colgrade_at_all = colgrades_nb == 0
        for i in range(len(self.store)):
            pupil_grades = self.store[Gtk.TreePath(i)][GRADES].cols
            if (len(pupil_grades) and len(pupil_grades) == colgrades_nb
                    and pupil_grades[-1] != ''):
                lock_grades_btns = False
                break
        self.insert_button.set_sensitive(not editing and rows_nb <= 1
                                         and self.user_selected_col is None)
        self.paste_pupils_button.set_sensitive(
            not editing and rows_nb <= 1 and self.user_selected_col is None)
        self.paste_grades_button.set_sensitive(not editing and len(self.store)
                                               and rows_nb <= 1
                                               and (no_colgrade_at_all
                                                    or not lock_grades_btns))
        self.add_grade_button.set_sensitive(not editing and len(self.store)
                                            and rows_nb <= 1
                                            and (no_colgrade_at_all
                                                 or not lock_grades_btns)
                                            and self.user_selected_col is None)
        self.edit_level_button.set_sensitive(rows_nb >= 2)
        self.edit_class_button.set_sensitive(rows_nb >= 1
                                             and len(self.classes) >= 2
                                             and not editing)

    def __add_grade_col(self, nth):
        """nth is the number of the grade (int starting from 0)"""
        grade = Gtk.CellRendererText()
        grade.props.editable = True
        grade.props.editable_set = True
        grade.props.max_width_chars = self.grades_cell_width
        grade.set_alignment(0.5, 0.5)
        grade.connect('editing-canceled', self.on_editing_canceled)
        grade.connect('editing-started', self.on_editing_started)
        grade.props.foreground_set = True

        def _set_cell_text(column, cell, model, it, index):
            obj = model.get_value(it, GRADES)
            if index < len(obj.cols):
                cell_text = obj.cols[index]
                cell.set_property('text', cell_text)
                color, weight = cellfont_fmt(cell_text,
                                             self.special_grades,
                                             self.grading)
                cell.set_property('foreground', color)
                cell.set_property('weight', weight)
            else:
                cell.set_property('text', '')

        col_grades = Gtk.TreeViewColumn('#{}'.format(nth + 1), grade)
        col_grades.grade_nb = nth
        col_grades.set_min_width(80)
        col_grades.set_alignment(0.5)
        col_grades.set_clickable(True)
        col_grades.connect('clicked', self.on_column_clicked)
        col_grades.set_cell_data_func(grade, _set_cell_text, nth)
        self.treeview.append_column(col_grades)

        setattr(self, 'gradecell{}'.format(nth), grade)
        getattr(self, 'gradecell{}'.format(nth)).connect(
            'edited', self.on_grade_edited)

    def on_key_release(self, widget, ev, data=None):
        if ev.keyval == Gdk.KEY_Escape:
            if self.started_insertion:
                self.cancel_insertion()
            if self.started_edition or self.started_insertion:
                self.post_edit_cleanup()
            self.set_buttons_sensitivity()
            if self.user_selected_col is not None:
                self.unselect_col(self.get_selected_col())

    def on_tree_selection_changed(self, selection):
        ListManagerBase.set_buttons_sensitivity(self)
        if self.user_selected_col is not None:
            self.unselect_col(self.get_selected_col())
            self.unselected_rows = None
        self.set_buttons_sensitivity()

    def on_paste_grades_clicked(self, widget):
        # TODO: factorize at least parts of this method with
        # on_paste_pupils_clicked
        text = self.clip.wait_for_text()
        if text is None:
            text = self.clip2.wait_for_text()
        if text is not None:
            PREFS = shared.PREFS
            tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext

            if '\t' in text:
                sep = '\t'
            else:
                sep = '\n'
            lines = text.strip().split(sep)

            do_paste = True
            # LATER: (when showing data before pasting) MAYBE allow less grades
            # than pupils
            if len(self.store) != len(lines):
                do_paste = False
                if len(self.store) > len(lines):
                    msg = tr('There are too few grades.\nIt is required to '
                             'paste as many grades as pupils.')
                else:
                    msg = tr('There are too many grades.\nIt is required to '
                             'paste as many grades as pupils.')
                run_message_dialog(tr('Number of pupils and grades mismatch'),
                                   msg, 'dialog-warning')

            for grade in lines:
                try:
                    self.check_user_entry(
                        grade, forbid_empty_cell=False,
                        forbid_duplicate_content=False,
                        forbid_internal_sep=True,
                        change_is_required=False)
                except ReservedCharsError:
                    do_paste = False
                    run_message_dialog(tr('Reserved group of characters'),
                                       tr('The group of characters "{}" has '
                                          'been found in the data you\'re '
                                          'about to paste, but it is reserved '
                                          'for internal use.\nPlease remove '
                                          'it from the data you want to paste '
                                          'before pasting again.\n'
                                          'Pasting grades cancelled.'
                                          ).format(SEP),
                                       'dialog-warning')

            if do_paste:
                names_list = [self.store[Gtk.TreePath(i)][FULLNAME]
                              for i in range(len(self.store))]
                if self.user_selected_col is None:
                    view = build_view([tr('Names')] + names_list,
                                      [tr('Grades')] + [L for L in lines],
                                      xalign=[0, 0.5])
                    msg = tr('Add following grades?')
                else:
                    col_num = self.user_selected_col
                    prev_grades_list = [
                        self.store[Gtk.TreePath(i)][GRADES]
                        .cols[col_num:col_num + 1] or ['']
                        for i in range(len(self.store))]
                    prev_grades_list = [item[0] for item in prev_grades_list]

                    def _set_cell_text(column, cell, model, it, ignored):
                        current = model.get_value(it, 1)
                        update = model.get_value(it, 2)
                        weight = int(Pango.Weight.NORMAL)
                        _, bgcolor, _, _ = get_theme_colors()
                        # LATER: appearance is poor, improve it!
                        if update != current:
                            weight = int(Pango.Weight.BOLD)
                            bgcolor = Gdk.RGBA()
                            bgcolor.parse('rgba(255, 179, 218, 255)')
                        cell.set_property('background_rgba', bgcolor)
                        cell.set_property('weight', weight)

                    view = build_view([tr('Names')] + names_list,
                                      [tr('Grade #{}')
                                       .format(self.user_selected_col + 1)]
                                      + prev_grades_list,
                                      [tr('Update')] + [L for L in lines],
                                      xalign=[0, 0.5, 0.5],
                                      set_cell_func=[None, None,
                                                     _set_cell_text])
                    msg = tr('Modify following grades?')
                conf_dialog = ConfirmationDialog(
                    tr('Please confirm'),
                    message=msg,
                    widget=view)
                response = conf_dialog.run()
                if response not in [Gtk.ResponseType.YES, Gtk.ResponseType.OK]:
                    do_paste = False
                conf_dialog.destroy()

            if do_paste:
                if self.user_selected_col is None:
                    self.__add_grade_col(self.grades_nb)
                    # cannot use self.grades_nb in the loop as it's updated
                    # at any commit
                    col_num = self.grades_nb
                else:
                    col_num = self.user_selected_col

                # Cursor change inspired by
                # https://stackoverflow.com/a/9881020/3926735
                self.get_window().set_cursor(
                    Gdk.Cursor.new_from_name(Gdk.Display.get_default(),
                                             'wait'))

                def add_grades(lines):
                    for i, grade in enumerate(lines):
                        # TODO: add a progression bar too, at bottom
                        path = Gtk.TreePath(i)
                        id_value = self.store[path][ID]
                        self.store[path][GRADES] = \
                            Listing(grade,
                                    data_row=self.store[path][GRADES].cols,
                                    position=col_num)
                        self.store[path][ALEVEL] = calculate_attained_level(
                            self.store[path][ILEVEL], self.levels,
                            self.grading, self.store[path][GRADES],
                            self.special_grades)
                        self.commit_pupil(
                            id_value, ['grades', 'attained_level'])

                    self.emit('data-changed')

                    self.get_window().set_cursor(None)
                    return False

                GObject.idle_add(add_grades, lines)

                self.on_column_clicked(
                    self.treeview.get_column(GRADES + self.user_selected_col))

    def on_add_grade_clicked(self, widget):
        self.__add_grade_col(self.grades_nb)

        GLib.timeout_add(50, self.treeview.set_cursor,
                         Gtk.TreePath(0),
                         self.treeview.get_column(GRADES + self.grades_nb),
                         True)

    def on_insert_clicked(self, widget):
        if not self.started_insertion:
            ListManagerBase.on_insert_clicked(
                self, widget, at='top', col_nb=2,
                do_scroll=(self.scrollable_treelist, Gtk.ScrollType.START,
                           False))
            self.set_buttons_sensitivity()

    def on_paste_pupils_clicked(self, widget):
        text = self.clip.wait_for_text()
        if text is None:
            text = self.clip2.wait_for_text()
        if text is not None:
            PREFS = shared.PREFS
            tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext

            if '\t' in text:
                sep = '\t'
            else:
                sep = '\n'
            lines = text.strip().split(sep)

            display_empty_lines_warning = False
            do_paste = True
            for name in lines:
                try:
                    self.check_user_entry(
                        name, forbid_empty_cell=True,
                        forbid_duplicate_content=False,
                        forbid_internal_sep=True,
                        change_is_required=False)
                except EmptyContentError:
                    display_empty_lines_warning = True
                except ReservedCharsError:
                    do_paste = False
                    run_message_dialog(tr('Reserved group of characters'),
                                       tr('The group of characters "{}" has '
                                          'been found in the data you\'re '
                                          'about to paste, but it is reserved '
                                          'for internal use.\nPlease remove '
                                          'it from the data you want to paste '
                                          'before pasting again.\n'
                                          'Pasting pupils\' names cancelled.'
                                          ).format(SEP),
                                       'dialog-warning')
            if do_paste:
                names_view = build_view([tr('Names')] + lines)
                conf_dialog = ConfirmationDialog(
                    tr('Please confirm'),
                    message=tr('Add following pupils?'),
                    widget=names_view)
                response = conf_dialog.run()
                if response not in [Gtk.ResponseType.YES, Gtk.ResponseType.OK]:
                    do_paste = False
                conf_dialog.destroy()

            if do_paste:
                # Cursor change inspired by
                # https://stackoverflow.com/a/9881020/3926735
                self.get_window().set_cursor(
                    Gdk.Cursor.new_from_name(Gdk.Display.get_default(),
                                             'wait'))

                if display_empty_lines_warning:
                    lines = [L for L in lines if L != '']
                    run_message_dialog(tr('Empty lines'),
                                       tr('The empty lines that have been '
                                          'found in the data you want to '
                                          'paste\nhave been automatically '
                                          'removed.'),
                                       'dialog-warning')

                def add_pupils(lines):
                    for name in lines:
                        # TODO: add a progression bar too, at bottom
                        fill_values = self.default_row_values
                        fill_values[FULLNAME] = name
                        self.store.insert(0, fill_values)
                        self.commit_pupil(None, ['fullname'])

                    self.emit('data-changed')

                    self.get_window().set_cursor(None)
                    return False

                GObject.idle_add(add_pupils, lines)

    def on_remove_clicked(self, widget):
        # TODO: ask before deleting a Pupil that already has grades
        p_ids = ListManagerBase.on_remove_clicked(self, widget, get_ids=0)
        removed = False
        for p_id in p_ids:
            if p_id not in ['', None]:
                shared.session.delete(shared.session.query(Pupils).get(p_id))
                removed = True
        if removed:
            shared.session.commit()
            shared.STATUS.document_modified = True
            self.emit('data-changed')
            self.set_buttons_sensitivity()

    def on_edit_level_clicked(self, widget):
        PREFS = shared.PREFS
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
        dialog = ComboDialog(tr('Change initial level'),
                             '', self.levels)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            model, paths = self.selection.get_selected_rows()
            for path in paths:
                self.on_initial_level_edited(widget, path, dialog.choice)
        dialog.destroy()

    def on_edit_class_clicked(self, widget):
        PREFS = shared.PREFS
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
        other_classes = [label
                         for label in self.classes
                         if label != self.classname]
        dialog = ComboDialog(tr('Move to another class'),
                             '', other_classes)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            model, paths = self.selection.get_selected_rows()
            for ref in paths:
                path = Gtk.TreeRowReference.new(model, ref).get_path()
                self.store[path][CLASS] = dialog.choice
                self.commit_pupil(self.store[path][ID], ['classname'])
                print('DATA TO MOVE: {}'
                      .format([str(self.store[path][ID]),
                               *self.store[path][CLASS:]]))
                gui.app.window.pupils_progression_manager_page\
                    .panels[dialog.choice].store.append(
                        [str(self.store[path][ID]), *self.store[path][CLASS:]])
                self.store.remove(self.store.get_iter(path))
            shared.STATUS.document_modified = True
            self.emit('data-changed')
        dialog.destroy()

    def get_selected_col(self):
        return self.treeview.get_column(GRADES + self.user_selected_col)

    def select_col(self, col):
        _, _, fg, bg = get_theme_colors()  # only the "selected" colors
        fg = convert_gdk_rgba_to_hex(fg)
        bg = convert_gdk_rgba_to_hex(bg)
        self.user_selected_col = col.grade_nb
        selected_title = Gtk.Label()
        selected_title.set_markup(
            r'<span fgcolor="{}" bgcolor="{}">{}</span>'
            .format(fg, bg, '#{}'.format(col.grade_nb + 1)))
        col.set_widget(selected_title)
        selected_title.show()
        self.renderer_name.props.editable = False

    def unselect_col(self, col):
        col.set_widget(None)
        col.set_title('#{}'.format(col.grade_nb + 1))
        self.user_selected_col = None
        self.renderer_name.props.editable = True

    def on_column_clicked(self, col):
        if self.unselected_rows is None:
            self.unselected_rows = \
                [t.to_string() for t in self.selection.get_selected_rows()[1]]
        self.selection.unselect_all()
        if self.user_selected_col is None:  # no selected col yet
            self.select_col(col)
        else:
            if col.grade_nb == self.user_selected_col:  # unselect col
                self.unselect_col(col)
                if self.unselected_rows is not None:  # give selection back
                    for i in self.unselected_rows:
                        self.selection.select_path(Gtk.TreePath(int(i)))
                self.unselected_rows = None
            else:  # change selected col
                prev_col = self.get_selected_col()
                new_col = col
                self.unselect_col(prev_col)
                self.select_col(new_col)
        self.set_buttons_sensitivity()
        # LATER: Also the col's cells should become selected.
        # Toggle the remove grade button to sensitive and use the current
        # selected col to remove a grade.

    def on_name_edited(self, widget, path, new_text):
        accepted, id_value = self.on_cell_edited(
            widget, path, new_text, forbid_empty_cell=True, col_nb=FULLNAME,
            forbid_duplicate_content=False, forbid_internal_sep=False)

        if accepted:
            self.commit_pupil(id_value, ['fullname'])
            self.emit('data-changed')
            self.set_buttons_sensitivity()

    def on_included_toggled(self, cell_renderer, path):
        self.store[path][INCLUDED] = not self.store[path][INCLUDED]
        self.commit_pupil(self.store[path][ID], ['included'])
        shared.STATUS.document_modified = True
        self.emit('data-changed')

    def on_initial_level_edited(self, widget, path, new_text):
        if new_text != self.store[path][ILEVEL]:
            ilevel = new_text
            self.store[path][ILEVEL] = ilevel
            grades = self.store[path][GRADES]
            shared.STATUS.document_modified = True
            self.store[path][ALEVEL] = calculate_attained_level(
                ilevel, self.levels, self.grading, grades, self.special_grades)
            self.commit_pupil(self.store[path][ID],
                              ['initial_level', 'attained_level'])
            self.emit('data-changed')
        self.post_edit_cleanup()
        self.set_buttons_sensitivity()

    def on_grade_edited(self, widget, path, new_text):
        id_value, model, treeiter, row = self.get_selection_info()
        pupil = shared.session.query(Pupils).get(id_value)
        col = self.treeview.get_cursor()[1]
        if pupil.grades is None:
            kwargs = None
        else:
            kwargs = {'data_row': pupil.grades, 'position': col.grade_nb}
        last_row = None
        if self.treeview.get_visible_range() is not None:
            last_row = self.treeview.get_visible_range()[1]
        accepted, id_value = \
            self.on_cell_edited(widget, path, new_text, col_nb=GRADES,
                                forbid_empty_cell=False,
                                forbid_duplicate_content=False,
                                do_cleanup=False,
                                cell_store_type=Listing,
                                cell_store_kwargs=kwargs)
        if accepted:
            self.store[path][ALEVEL] = calculate_attained_level(
                pupil.initial_level, self.levels, self.grading,
                self.store[path][GRADES], self.special_grades)
            self.commit_pupil(id_value, ['grades', 'attained_level'])
            time.sleep(0.1)
            self.emit('data-changed')
            if col is not None and last_row is not None:
                position = int(row.to_string())
                last_position = int(last_row.to_string())
                next_val = 'undefined'  # Could be any str except ''
                while position < last_position:
                    next_row = Gtk.TreePath(position + 1)
                    try:
                        next_val = self.store[next_row][GRADES]\
                            .cols[col.grade_nb]
                    except IndexError:
                        next_val = ''
                    if next_val in ['', None]:
                        break
                    else:
                        position += 1
                if next_val in ['', None]:
                    GLib.timeout_add(50, self.treeview.set_cursor,
                                     next_row, col, True)
                else:
                    self.on_editing_canceled(None)
        else:  # Unaccepted text (e.g. internal separator was rejected)
            # Simply set cursor on the same cell again
            GLib.timeout_add(50, self.treeview.set_cursor, row, col, True)

    def commit_pupil(self, id_value, attrnames=None):
        # TODO: add a method that would do most of this job, but not commit
        # (like 'add_pupil'), that this method would re-use in order to
        # commit. This would be helpful in cases where a bunch of pupils is
        # added at once (then only one commit at the end).
        # Or maybe a unique method that would deal with a bunch of pupils?
        _, path = self.get_path_from_id(id_value)
        new = False
        if attrnames is None:
            attrnames = []
        if id_value in ['', None]:
            new = True
            pupil = Pupils(classname=self.classname,
                           included=self.store[path][INCLUDED],
                           fullname=self.store[path][FULLNAME],
                           initial_level=self.store[path][ILEVEL],
                           attained_level=self.store[path][ALEVEL],
                           grades=self.store[path][GRADES])
            shared.session.add(pupil)
        else:
            pupil = shared.session.query(Pupils).get(id_value)
            for attrname in attrnames:
                col_nb = PUPILS_COL_NBS[attrname]
                setattr(pupil, attrname, self.store[path][col_nb])
        shared.session.commit()
        shared.STATUS.document_modified = True
        if new:
            self.store[path][ID] = str(pupil.id)
