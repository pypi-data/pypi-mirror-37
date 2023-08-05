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

from gettext import translation

from mathmakerlib.calculus import Number

import gi
try:
    gi.require_version('Gtk', '3.0')
except ValueError:
    raise
else:
    from gi.repository import Gtk

from cotinga.core import shared
from cotinga.core.env import LOCALEDIR, L10N_DOMAIN
from cotinga.gui.panels import ListManagerPanel
from cotinga.data.default.data.pmdoc.presets import GRADES_SCALES


class LiteralGradingPanel(ListManagerPanel):

    def __init__(self, grading_setup):
        PREFS = shared.PREFS
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
        ListManagerPanel.__init__(self, grading_setup['literal_grades'],
                                  tr('Labels'),
                                  presets=(GRADES_SCALES(),
                                           tr('Load a preset scale'),
                                           tr('Replace current scale '
                                              'by: '),
                                           'insert-text'))

        self.current_edge = grading_setup['edge_literal']
        self.edges_store = Gtk.ListStore(str)
        self.len_edges_store = 0
        self.currently_selected = 0

        self.update_edges_store()

        self.combo = Gtk.ComboBox.new_with_model(self.edges_store)

        renderer = Gtk.CellRendererText()
        self.combo.pack_start(renderer, False)
        self.combo.add_attribute(renderer, 'text', 0)

        self.combo.set_active(self.currently_selected)
        self.combo.set_margin_top(7)
        self.combo.set_margin_left(10)
        # combo.connect('changed', self.on_choice_changed)

        combo_grid = Gtk.Grid()
        combo_label = Gtk.Label(tr('Edge:'))
        combo_label.set_margin_top(7)
        combo_grid.attach(combo_label, 0, 0, 1, 1)
        combo_grid.attach_next_to(self.combo, combo_label,
                                  Gtk.PositionType.RIGHT, 1, 1)
        self.attach_next_to(combo_grid, self.buttons_grid,
                            Gtk.PositionType.RIGHT, 1, 1)
        self.combo.connect('changed', self.on_edge_choice_changed)
        self.connect('data_changed', self.on_data_changed)

    def update_edges_store(self):
        # Remove current edges list
        for i in range(len(self.edges_store)):
            treeiter = self.edges_store.get_iter(Gtk.TreePath(0))
            self.edges_store.remove(treeiter)

        # Rebuild list from scratch
        entries = [row[0] for row in self.store]
        entries = entries[:-1]
        for entry in entries:
            self.edges_store.append([entry])

        # Find out the best new selection: either we keep the previous value,
        # or try to stick close to it, or set to 0.
        new_selection = None
        for i, edge in enumerate(entries):
            if edge == self.current_edge:
                new_selection = i
        if new_selection is None:
            new_selection = int(Number((self.currently_selected
                                        / self.len_edges_store)
                                       * len(self.edges_store))
                                .rounded(Number(1)))
        if new_selection < 0:
            new_selection = 0

        self.currently_selected = new_selection
        self.len_edges_store = len(self.edges_store)

    def on_data_changed(self, *args):
        self.update_edges_store()
        self.combo.set_active(self.currently_selected)

    def on_edge_choice_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            self.current_edge = model[tree_iter][0]
            entries = [row[0] for row in self.edges_store]
            new_selection = None
            for i, edge in enumerate(entries):
                if edge == self.current_edge:
                    new_selection = i
            if new_selection is not None:
                self.currently_selected = new_selection
