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
except ValueError:
    raise
else:
    from gi.repository import GLib, Gdk, Gtk, GObject

from cotinga.core import shared, pmdoc
from cotinga.core.env import LOCALEDIR, L10N_DOMAIN
from cotinga.core.env import ICON_THEME
from cotinga.core.errors import CotingaError, DuplicateContentError
from cotinga.core.errors import EmptyContentError, ReservedCharsError
from cotinga.core.errors import NoChangeError
from cotinga.gui.dialogs import run_message_dialog
from cotinga.gui.core import IconsThemable
from cotinga.core import constants

SEP = constants.INTERNAL_SEPARATOR


class __MetaThemableGrid(type(Gtk.Grid), type(IconsThemable)):
    pass


class ListManagerBase(Gtk.Grid, IconsThemable, metaclass=__MetaThemableGrid):

    @GObject.Signal
    def data_changed(self):
        """Notify that data stored in self.store have changed."""

    def __init__(self, setup_buttons_icons=True, mini_items_nb=2,
                 store_types=None, locked=None):
        Gtk.Grid.__init__(self)
        IconsThemable.__init__(self)
        self.set_column_spacing(10)
        self.set_vexpand(True)
        self.set_hexpand(True)
        self.mini_items_nb = mini_items_nb
        if store_types is None:
            store_types = [str]
        if locked is None:
            self.locked = []
        else:
            self.locked = locked

        self.store = Gtk.ListStore(*store_types)

        self.treeview = Gtk.TreeView(self.store)
        self.treeview.props.margin = 10
        self.selection.set_mode(Gtk.SelectionMode.MULTIPLE)

        self.insert_button = Gtk.ToolButton.new()
        self.remove_button = Gtk.ToolButton.new()

        self.selection.connect('changed', self.on_tree_selection_changed)

        self.new_row_position = None

        # Also helps to block repeated pushes on 'insert' (setting sensitive
        # to False does not work from inside on_insert_clicked())
        self.started_insertion = False
        self.started_edition = False

        self.connect('key-release-event', self.on_key_release)

        docsetup = pmdoc.setting.load()
        self.levels = docsetup['levels']
        self.classes = docsetup['classes']
        self.special_grades = docsetup['special_grades']
        self.grading = docsetup['grading']

        if setup_buttons_icons:
            self.setup_buttons_icons(ICON_THEME)

    @property
    def selection(self):
        return self.treeview.get_selection()

    def buttons_icons(self):
        """Defines icon names and fallback to standard icon name."""
        # Last item of each list is the fallback, hence must be standard
        buttons = {'insert_button': ['list-add'],
                   'remove_button': ['list-remove']}
        return buttons

    def buttons_labels(self):
        """Define labels of buttons."""
        PREFS = shared.PREFS
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
        buttons = {'insert_button': tr('Add'),
                   'remove_button': tr('Remove')
                   }
        return buttons

    def set_buttons_sensitivity(self):
        selected = self.selection.get_selected_rows()[1]
        if selected:
            unlocked = self.store[selected][0] not in self.locked
        else:
            unlocked = False  # nothing is selected, anyway
        editing = self.started_insertion or self.started_edition
        minimum_required = len(self.store) >= self.mini_items_nb + 1
        self.remove_button.set_sensitive(selected and unlocked
                                         and minimum_required
                                         and not editing)
        self.insert_button.set_sensitive(not editing)

    def on_key_release(self, widget, ev, data=None):
        if ev.keyval == Gdk.KEY_Escape and self.started_insertion:
            self.cancel_insertion()
            self.post_edit_cleanup()

    def on_editing_started(self, cell_renderer, editable, path):
        if self.selection.count_selected_rows() >= 2:
            # This will trigger an edit canceled and select the current row
            # instead.
            GLib.timeout_add(50, self.selection.unselect_all)
            GLib.timeout_add(60, self.selection.select_path, path)
        self.started_edition = True
        self.set_buttons_sensitivity()

    def on_editing_canceled(self, cell_renderer):
        if self.started_insertion:
            self.cancel_insertion()
        self.post_edit_cleanup()
        self.set_buttons_sensitivity()

    def on_insert_clicked(self, widget, at='selection', col_nb=0,
                          override_defaults=None, do_scroll=None):
        # In case of multiple rows selection, we only take the first one
        # into account
        model, treepath = self.selection.get_selected_rows()
        self.started_insertion = True
        fill_values = getattr(self, 'default_row_values', None)
        if override_defaults is not None:
            for i, value in enumerate(override_defaults):
                if value is not None:
                    fill_values[i] = value
        if at == 'selection' and treepath:
            path = treepath[0]
            position = int(treepath[0].to_string())
        else:  # default (e.g. no selection available or at != 'selection')
            #    => at top of the list
            position = 0
            path = Gtk.TreePath(position)

        self.store.insert(position, fill_values)
        self.new_row_position = position
        GLib.timeout_add(50, self.treeview.set_cursor, path,
                         self.treeview.get_column(col_nb), True)
        time.sleep(0.06)
        if do_scroll is not None:
            scrollable_window = do_scroll[0]
            scrollable_window.do_scroll_child(*do_scroll)
        self.set_buttons_sensitivity()

    def on_remove_clicked(self, widget, get_ids=None):
        model, paths = self.selection.get_selected_rows()
        refs = []
        id_values = []
        for path in paths:
            refs.append(Gtk.TreeRowReference.new(model, path))
        for ref in refs:
            path = ref.get_path()
            treeiter = model.get_iter(path)
            value = model.get(treeiter, 0)[0]
            if hasattr(model, 'remove'):
                if isinstance(get_ids, int):
                    id_values.append(model.get(treeiter, 0)[get_ids])
                model.remove(treeiter)
            else:  # Case of filtered or sortered models
                #    => Usage of get_ids is mandatory
                if not isinstance(get_ids, int):
                    raise CotingaError('For a TreeModel that does not '
                                       'implement remove(), it is mandatory '
                                       'to provide the column number that '
                                       'will be the key to find the row(s) to '
                                       'remove.')
                for i, row in enumerate(self.store):
                    if row[get_ids] == value:
                        rowpath = Gtk.TreePath(i)
                        treeiter = self.store.get_iter(rowpath)
                        if isinstance(get_ids, int):
                            id_values.append(
                                self.store.get_value(treeiter, get_ids))
                        self.store.remove(treeiter)

        self.started_insertion = False
        self.emit('data-changed')
        self.post_edit_cleanup()
        if isinstance(get_ids, int):
            return id_values

    def on_tree_selection_changed(self, selection):
        self.set_buttons_sensitivity()

    def cancel_insertion(self):
        if self.new_row_position is not None and self.started_insertion:
            path = Gtk.TreePath(self.new_row_position)
            treeiter = self.store.get_iter(path)
            self.store.remove(treeiter)

    def post_edit_cleanup(self, do_cleanup=True):
        if do_cleanup:
            self.started_insertion = False
            self.started_edition = False
            self.new_row_position = None
            self.set_buttons_sensitivity()

    def get_path_from_id(self, id_value, idcol=0):
        rowpath = None
        for i, row in enumerate(self.store):
            if row[idcol] == id_value:
                rowpath = Gtk.TreePath(i)
                break
        return (i, rowpath)

    def get_selection_info(self):
        model, paths = self.selection.get_selected_rows()
        ref = Gtk.TreeRowReference.new(model, paths[0])
        path = ref.get_path()
        treeiter = model.get_iter(path)
        id_value = model.get(treeiter, 0)[0]
        return (id_value, model, treeiter, path)

    def check_user_entry(self, new_text, old_text=None, forbid_empty_cell=True,
                         forbid_duplicate_content=True,
                         forbid_internal_sep=True, change_is_required=True):
        if forbid_empty_cell and new_text == '':
            raise EmptyContentError
        elif change_is_required and new_text == old_text:
            raise NoChangeError
        elif (forbid_duplicate_content
                and any([row[0] == new_text for row in self.store])):
            raise DuplicateContentError(new_text)
        elif forbid_internal_sep and SEP in new_text:
            raise ReservedCharsError(new_text)

    def on_cell_edited(self, widget, path, new_text, col_nb=0,
                       forbid_empty_cell=True,
                       forbid_duplicate_content=True,
                       forbid_internal_sep=True,
                       change_is_required=True,
                       do_cleanup=True,
                       cell_store_type=None,
                       cell_store_kwargs=None):
        id_value, model, treeiter, _ = self.get_selection_info()
        rowpath = None
        print('[on_cell_edited] start')
        accepted = False
        old_text = model.get(treeiter, col_nb)[0]
        PREFS = shared.PREFS
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
        try:
            self.check_user_entry(
                new_text, old_text=old_text,
                forbid_empty_cell=forbid_empty_cell,
                forbid_duplicate_content=forbid_duplicate_content,
                forbid_internal_sep=forbid_internal_sep,
                change_is_required=change_is_required)
        except EmptyContentError:
            if self.started_insertion:
                self.cancel_insertion()
        except NoChangeError:
            pass  # Will leave the new content not accepted
        except DuplicateContentError:
            run_message_dialog(tr('No duplicates!'),
                               tr('Each label must be unique.\n'
                                  'Modification cancelled.'),
                               'dialog-warning')
            self.cancel_insertion()
        except ReservedCharsError:
            run_message_dialog(tr('Reserved group of characters'),
                               tr('The group of characters "{}" is '
                                  'reserved for internal use, you '
                                  'cannot use them here, sorry.\n'
                                  'Modification cancelled.'
                                  ).format(SEP),
                               'dialog-warning')
            self.cancel_insertion()
        else:
            _, rowpath = self.get_path_from_id(id_value)
            if rowpath is not None:
                if cell_store_type is not None:
                    new_text = cell_store_type(new_text,
                                               **(cell_store_kwargs or {}))
                self.store[rowpath][col_nb] = new_text
                print('\nSTORED {}'.format(new_text))
                accepted = True
                self.emit('data-changed')
        self.post_edit_cleanup(do_cleanup)
        print('[on_cell_edited] return accepted={}'.format(accepted))
        return (accepted, id_value)
