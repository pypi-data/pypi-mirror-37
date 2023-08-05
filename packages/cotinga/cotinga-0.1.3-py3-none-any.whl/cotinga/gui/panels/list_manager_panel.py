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

import gi
try:
    gi.require_version('Gtk', '3.0')
except ValueError:
    raise
else:
    from gi.repository import Gtk

from cotinga.gui.dialogs import PresetsComboDialog
from .list_manager_base import ListManagerBase


class ListManagerPanel(ListManagerBase):

    def __init__(self, data_list, data_title, mini_items_nb=2, presets=None,
                 locked=None, store_types=None, reorderable=True,
                 editable=None):
        """
        presets is either None or (source, title, message, icon_name)
        where source is the presets dictionary (see data/presets.py),
        title and message are str that contain the title and the message of the
        combo dialog,
        icon_name is the name of the presets button to display.
        """
        ListManagerBase.__init__(self, mini_items_nb=mini_items_nb,
                                 locked=locked, store_types=store_types)

        if store_types is None:
            store_types = [str]

        if editable is None:
            editable = [True] * len(store_types)

        self.data_list = data_list

        for item in self.data_list:
            if isinstance(item, tuple):
                self.store.append(list(item))
            else:
                self.store.append([item])

        for i in range(len(store_types)):
            rend = Gtk.CellRendererText()
            rend.props.editable = editable[i]
            rend.props.editable_set = editable[i]
            if editable[i]:
                rend.connect('edited', self.on_cell_edited)
            rend.connect('editing-started', self.on_editing_started)
            rend.connect('editing-canceled', self.on_editing_canceled)
            if isinstance(data_title, (list, tuple)):
                col_title = data_title[i]
            else:
                col_title = data_title
            column = Gtk.TreeViewColumn(col_title, rend, text=i)
            self.treeview.append_column(column)

        self.treeview.set_reorderable(reorderable)

        self.attach(self.treeview, 0, 0, 1, 1)

        self.buttons_grid = Gtk.Grid()
        self.buttons_grid.props.margin = 10

        self.presets = presets
        if presets is not None:
            (self.presets_source, self.presets_title, self.presets_message,
             self.preset_icon_name) = \
                presets
            self.load_presets_button = \
                Gtk.Button.new_from_icon_name(self.preset_icon_name,
                                              Gtk.IconSize.BUTTON)
            self.load_presets_button.set_vexpand(False)
            self.load_presets_button.set_sensitive(True)
            self.load_presets_button.connect('clicked',
                                             self.on_load_presets_clicked)
            sep = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
            sep.set_margin_bottom(10)
            sep.set_margin_top(10)
            self.buttons_grid.attach(self.load_presets_button, 0, 0, 1, 1)
            self.buttons_grid.attach_next_to(sep, self.load_presets_button,
                                             Gtk.PositionType.BOTTOM, 1, 1)
            previous = sep
        else:
            void = Gtk.Grid()
            void.set_vexpand(False)
            void.set_margin_bottom(20)
            self.buttons_grid.attach(void, 0, 0, 1, 1)
            previous = void

        self.insert_button.set_vexpand(False)
        self.insert_button.connect('clicked', self.on_insert_clicked)
        self.insert_button.set_margin_bottom(10)
        self.buttons_grid.attach_next_to(self.insert_button, previous,
                                         Gtk.PositionType.BOTTOM, 1, 1)

        self.remove_button.set_vexpand(False)
        self.remove_button.set_sensitive(False)
        self.remove_button.connect('clicked', self.on_remove_clicked)
        self.buttons_grid.attach_next_to(self.remove_button,
                                         self.insert_button,
                                         Gtk.PositionType.BOTTOM, 1, 1)

        self.attach_next_to(self.buttons_grid, self.treeview,
                            Gtk.PositionType.RIGHT, 1, 1)

    def on_load_presets_clicked(self, widget):
        dialog = PresetsComboDialog(self.presets_title, self.presets_message,
                                    self.presets_source)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.store.clear()
            for item in dialog.choice:
                self.store.append([item])
        dialog.destroy()
        self.emit('data-changed')
