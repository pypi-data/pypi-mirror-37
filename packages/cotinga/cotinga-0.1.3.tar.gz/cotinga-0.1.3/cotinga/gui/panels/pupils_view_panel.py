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

from shutil import copyfile
from gettext import translation
from sqlalchemy.sql import false
from sqlalchemy.sql.expression import or_, and_

import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('Poppler', '0.18')
except ValueError:
    raise
else:
    from gi.repository import Gtk, GObject, Poppler

from cotinga.core.env import LOCALEDIR, L10N_DOMAIN
from cotinga.core.env import REPORT_FILE, REPORT_FILE_URI
from cotinga.core.env import ICON_THEME, get_theme_colors
from cotinga.core.tools import Listing, cellfont_fmt
from cotinga.core.pmdoc import report
from cotinga.core import shared
from cotinga.models import Pupils
from cotinga.gui.panels import ListManagerBase
from cotinga import gui
from cotinga.core import constants
from cotinga.gui.dialogs import PreviewDialog, SaveAsFileDialog

STEPS = constants.NUMERIC_STEPS

# Column numbers of the store
ID, INCLUDED, CLASS, FULLNAME, ILEVEL, ALEVEL, GRADES = (0, 1, 2, 3, 4, 5, 6)


class PupilsViewPanel(ListManagerBase):

    def __init__(self):
        ListManagerBase.__init__(self, setup_buttons_icons=False,
                                 mini_items_nb=0,
                                 store_types=[str, bool, str, str, str, str,
                                              GObject.TYPE_PYOBJECT])
        PREFS = shared.PREFS
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext

        self.pupils_nb = 0

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

        self.refresh_data()
        self.class_filter = self.store.filter_new()
        self.class_filter.set_visible_func(self.class_filter_func)
        self.sorted_and_filtered_model = \
            Gtk.TreeModelSort(model=self.class_filter)
        self.sorted_and_filtered_model.set_sort_column_id(
            FULLNAME, Gtk.SortType.ASCENDING)
        self.treeview = Gtk.TreeView.new_with_model(
            self.sorted_and_filtered_model)

        # As original treeview is modified, it's necessary to reconnect it
        self.selection.connect('changed', self.on_tree_selection_changed)
        self.selection.set_mode(Gtk.SelectionMode.MULTIPLE)

        # TODO: remove this code duplication (see pupils manager panel)
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
        self.col_incl = Gtk.TreeViewColumn(tr('Included'), self.renderer_incl,
                                           active=1)
        self.col_incl.set_visible(shared.STATUS.show_col_incl)

        self.renderer_class = Gtk.CellRendererText()
        col_class = Gtk.TreeViewColumn(tr('Class'), self.renderer_class,
                                       text=2)
        col_class.set_cell_data_func(self.renderer_class,
                                     _set_cell_fgcolor, '')
        col_class.set_sort_column_id(2)

        self.renderer_name = Gtk.CellRendererText()
        col_name = Gtk.TreeViewColumn(tr('Name'), self.renderer_name, text=3)
        col_name.set_cell_data_func(self.renderer_name, _set_cell_fgcolor, '')
        col_name.set_sort_column_id(3)

        self.renderer_ilevel = Gtk.CellRendererText()
        self.col_ilevel = Gtk.TreeViewColumn(tr('Initial level'),
                                             self.renderer_ilevel, text=4)
        self.col_ilevel.set_cell_data_func(self.renderer_ilevel,
                                           _set_cell_fgcolor, '')
        self.col_ilevel.set_visible(shared.STATUS.show_col_ilevel)
        self.col_ilevel.set_sort_column_id(4)

        self.renderer_alevel = Gtk.CellRendererText()
        col_alevel = Gtk.TreeViewColumn(tr('Attained level'),
                                        self.renderer_alevel,
                                        text=5)
        col_alevel.set_cell_data_func(self.renderer_alevel,
                                      _set_cell_fgcolor, '')
        col_alevel.set_sort_column_id(5)

        for i, col in enumerate([self.col_id, self.col_incl, col_class,
                                 col_name, self.col_ilevel, col_alevel]):
            # TODO: do not set a minimum width (or not hardcoded at least)
            # instead, check properties of Gtk.TreeViewColumn objects and see
            # what's possible
            # col.set_min_width(100)
            self.treeview.append_column(col)

        self.add_missing_cols()

        # LATER: remove this code duplication with pupils_manager_panel
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

        info_frame = Gtk.Frame()
        frame_content = Gtk.Grid()
        self.info_pupils_nb = Gtk.Label()
        self.info_pupils_nb.props.margin = 5
        self.info_pupils_nb.props.margin_bottom = 8
        self.info_pupils_dist = Gtk.Label()
        self.info_pupils_dist.props.margin = 5
        self.report_data = []
        self.refresh_info()
        frame_content.attach(self.info_pupils_nb, 0, 0, 1, 1)
        frame_content.attach_next_to(self.info_pupils_dist,
                                     self.info_pupils_nb,
                                     Gtk.PositionType.BOTTOM, 1, 1)
        self.preview_button = Gtk.ToolButton.new()
        self.preview_button.set_vexpand(False)
        self.preview_button.set_halign(Gtk.Align.CENTER)
        self.preview_button.set_valign(Gtk.Align.CENTER)
        self.preview_button.connect('clicked', self.on_preview_clicked)
        frame_content.attach_next_to(self.preview_button,
                                     self.info_pupils_dist,
                                     Gtk.PositionType.BOTTOM, 1, 1)
        info_frame.add(frame_content)
        self.attach_next_to(info_frame, self.scrollable_treelist,
                            Gtk.PositionType.RIGHT, 1, 1)

        # BOTTOM TOOLS (filters)
        self.bottom_tools = Gtk.Grid()
        self.bottom_tools.set_hexpand(False)
        self.bottom_tools.props.margin_bottom = 0
        self.bottom_tools.props.margin_top = 3

        self.filters_label = Gtk.Label(tr('Visible classes:'))
        self.filters_label.set_margin_left(5)
        self.filters_label.set_margin_right(10)
        self.bottom_tools.attach(self.filters_label, 0, 0, 1, 1)

        # LATER: make displaying no_filter and all_filters buttons be an option
        self.no_filter = Gtk.Button(tr('None'))
        self.no_filter.connect('clicked', self.on_no_filter_button_clicked)
        self.no_filter.set_margin_right(3)
        self.bottom_tools.attach_next_to(self.no_filter,
                                         self.filters_label,
                                         Gtk.PositionType.RIGHT, 1, 1)

        self.all_filters = Gtk.Button(tr('All'))
        self.all_filters.connect('clicked', self.on_all_filters_button_clicked)
        self.all_filters.set_margin_right(3)
        self.bottom_tools.attach_next_to(self.all_filters,
                                         self.no_filter,
                                         Gtk.PositionType.RIGHT, 1, 1)

        self.filter_buttons = Gtk.Grid()
        self.build_filter_buttons()
        self.bottom_tools.attach_next_to(self.filter_buttons,
                                         self.all_filters,
                                         Gtk.PositionType.RIGHT, 1, 1)

        self.attach_next_to(self.bottom_tools, self.scrollable_treelist,
                            Gtk.PositionType.BOTTOM, 1, 1)

        bottomvoid_grid = Gtk.Grid()
        bottomvoid_grid.set_hexpand(True)
        self.attach_next_to(bottomvoid_grid, self.bottom_tools,
                            Gtk.PositionType.RIGHT, 1, 1)
        self.pdf_report = None
        self.setup_buttons_icons(ICON_THEME)
        self.setup_info_visibility()

    @property
    def grades_nb(self):
        # TODO: looks like it could be partially factorized with
        # pupils_manager_panel.grades_nb()
        all_pupils = shared.session.query(Pupils).all()
        return max([len(pupil.grades or []) for pupil in all_pupils] or [0])

    def buttons_icons(self):
        """Defines icon names and fallback to standard icon name."""
        # Last item of each list is the fallback, hence must be standard
        buttons = ListManagerBase.buttons_icons(self)
        buttons.update({'preview_button': ['application-pdf',
                                           'document-print-preview']})
        return buttons

    def buttons_labels(self):
        """Defines icon names and fallback to standard icon name."""
        # Last item of each list is the fallback, hence must be standard
        PREFS = shared.PREFS
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
        buttons = ListManagerBase.buttons_labels(self)
        buttons.update({'preview_button': tr('Preview')})
        return buttons

    def __build_report_data(self):
        PREFS = shared.PREFS
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
        constraints = []
        for classname in shared.STATUS.filters:
            constraints.append(Pupils.classname == classname)
        if constraints:
            # Making use of Pupils.included is True makes the filtering fail
            pupils = shared.session.query(Pupils).filter(
                and_(Pupils.included == True, or_(*constraints)))  # noqa
        else:
            pupils = shared.session.query(Pupils).filter(false())
        report_data = []
        for i, level in enumerate(self.levels):
            n = pupils.filter(Pupils.attained_level == level).count()
            if n:
                if i == len(self.levels) - 1:
                    next_level = level
                else:
                    next_level = self.levels[i + 1]
                pupils_list = pupils.filter(
                    Pupils.attained_level == level).all()
                report_data.append((next_level, n, pupils_list))
        pupils_dist = '\n'.join([tr('{level}: {number}')
                                 .format(level=item[0], number=item[1])
                                 for item in report_data])
        return (pupils.count(), pupils_dist, report_data)

    def refresh_info(self):
        PREFS = shared.PREFS
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
        self.pupils_nb, pupils_dist, self.report_data = \
            self.__build_report_data()
        self.info_pupils_nb.set_text(
            tr('Pupils\' number: {}').format(self.pupils_nb))
        self.info_pupils_dist.set_text(
            tr('Next evaluation:') + '\n' + pupils_dist)

    def setup_info_visibility(self):
        if self.pupils_nb:
            self.info_pupils_dist.show()
            self.preview_button.show()
        else:
            self.info_pupils_dist.hide()
            self.preview_button.hide()

    def refresh_data(self):
        # LATER: to avoid having to refresh data, use set_cell_func_data in
        # order to actually store "nothing" in the view's store, but have
        # permanent automatic refreshing instead
        self.store.clear()
        for pupil in shared.session.query(Pupils).all():
            self.store.append([str(pupil.id), pupil.included, pupil.classname,
                               pupil.fullname, pupil.initial_level,
                               pupil.attained_level, Listing(pupil.grades)])

    def add_missing_cols(self):
        current_nb = len(self.treeview.get_columns())
        missing = GRADES + self.grades_nb - current_nb
        offset = current_nb - GRADES
        for i in range(missing):
            grade = Gtk.CellRendererText()
            grade.props.max_width_chars = self.grades_cell_width
            grade.set_alignment(0.5, 0.5)

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

            col_grades = Gtk.TreeViewColumn(
                '#{}'.format(i + offset + 1), grade)
            col_grades.set_cell_data_func(grade, _set_cell_text, i + offset)
            setattr(self, 'gradecell{}'.format(i + offset), grade)
            # LATER: add sorting by grade (line below does not work)
            # col_grades.set_sort_column_id(GRADES + i + offset)
            col_grades.set_min_width(80)
            col_grades.set_alignment(0.5)
            self.treeview.append_column(col_grades)

    def refresh(self):
        self.refresh_data()
        self.add_missing_cols()
        self.refresh_info()
        self.setup_info_visibility()

    def build_filter_buttons(self):
        """Build the filter buttons according to available classes."""
        for btn in self.filter_buttons.get_children():
            self.filter_buttons.remove(btn)
        for classname in self.classes:
            button = Gtk.ToggleButton(classname)
            button.set_margin_right(3)
            button.connect('toggled', self.on_filter_button_toggled)
            if classname in shared.STATUS.filters:
                button.set_active(True)
            else:
                button.set_active(False)
            self.filter_buttons.add(button)
        self.filter_buttons.show_all()

    def on_filter_button_toggled(self, widget):
        """Called on any of the filter button clicks"""
        classname = widget.get_label()
        if widget.get_active():
            shared.STATUS.filters = \
                list(set(shared.STATUS.filters + [classname]))
        else:
            shared.STATUS.filters = [label
                                     for label in shared.STATUS.filters
                                     if label != classname]
        self.class_filter.refilter()
        self.refresh_info()
        self.setup_info_visibility()

    def on_no_filter_button_clicked(self, widget):
        for btn in self.filter_buttons:
            btn.set_active(False)

    def on_all_filters_button_clicked(self, widget):
        for btn in self.filter_buttons:
            btn.set_active(True)

    def on_preview_clicked(self, widget):
        report.build(self.report_data)
        PREFS = shared.PREFS
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
        dialog = PreviewDialog(tr('Report preview'))
        response = dialog.run()

        if response == Gtk.ResponseType.YES:  # save as
            save_as_dialog = SaveAsFileDialog(report=True)
            save_as_response = save_as_dialog.run()
            if save_as_response == Gtk.ResponseType.OK:
                report_name = save_as_dialog.get_filename()
                copyfile(REPORT_FILE, report_name)
            save_as_dialog.destroy()
            dialog.destroy()
            self.on_preview_clicked(widget)

        elif response == Gtk.ResponseType.OK:  # print
            operation = Gtk.PrintOperation()
            operation.connect('begin-print', self.begin_print, None)
            operation.connect('draw-page', self.draw_page, None)
            self.pdf_report = Poppler.Document.new_from_file(REPORT_FILE_URI)
            print_setup = Gtk.PageSetup()
            print_setup.set_orientation(Gtk.PageOrientation.LANDSCAPE)
            print_setup.set_left_margin(7, Gtk.Unit.MM)
            print_setup.set_right_margin(7, Gtk.Unit.MM)
            print_setup.set_top_margin(7, Gtk.Unit.MM)
            print_setup.set_bottom_margin(7, Gtk.Unit.MM)
            operation.set_default_page_setup(print_setup)
            # print_settings = Gtk.PrintSettings()
            # print_settings.set_orientation(Gtk.PageOrientation.LANDSCAPE)
            # operation.set_print_settings(print_settings)
            print_result = operation.run(Gtk.PrintOperationAction.PRINT_DIALOG,
                                         gui.app.window)
            if print_result == Gtk.PrintOperationResult.ERROR:
                message = self.operation.get_error()
                errdialog = Gtk.MessageDialog(gui.app.window,
                                              0,
                                              Gtk.MessageType.ERROR,
                                              Gtk.ButtonsType.CLOSE,
                                              message)
                errdialog.run()
                errdialog.destroy()
            dialog.destroy()
            self.on_preview_clicked(widget)

        else:  # close or cancel, whatever
            dialog.destroy()

    def begin_print(self, operation, print_ctx, print_data):
        operation.set_n_pages(self.pdf_report.get_n_pages())

    def draw_page(self, operation, print_ctx, page_num, print_data):
        cr = print_ctx.get_cairo_context()
        page = self.pdf_report.get_page(page_num)
        page.render_for_printing(cr)

    def class_filter_func(self, model, treeiter, data):
        """Test if the class in the row is the one in the filter"""
        return model[treeiter][CLASS] in shared.STATUS.filters
