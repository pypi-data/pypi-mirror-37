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

import sys
import locale
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
from cotinga.core import constants

STEPS = constants.NUMERIC_STEPS


class NumericGradingPanel(Gtk.Grid):

    def __init__(self, grading_setup):
        Gtk.Grid.__init__(self)
        self.set_column_spacing(10)
        self.set_vexpand(True)
        self.set_hexpand(True)
        PREFS = shared.PREFS
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext

        self.minimum = grading_setup['minimum']
        self.maximum = grading_setup['maximum']
        self.edge = grading_setup['edge_numeric']
        self.step = Number(STEPS[grading_setup['step']])

        self.steps_store = Gtk.ListStore(str, str)
        for i, s in enumerate(STEPS):
            self.steps_store.append([str(i), locale.str(Number(STEPS[s]))])
        self.steps_combo = \
            Gtk.ComboBox.new_with_model(self.steps_store)
        self.steps_combo.props.margin_bottom = 5
        self.steps_combo.set_id_column(0)
        self.steps_combo.set_entry_text_column(1)
        renderer = Gtk.CellRendererText()
        self.steps_combo.pack_start(renderer, True)
        self.steps_combo.add_attribute(renderer, 'text', 1)
        self.steps_combo.set_active(grading_setup['step'])
        self.steps_combo.connect('changed', self.on_steps_combo_changed)

        self.minimum_button = Gtk.SpinButton()
        self.edge_button = Gtk.SpinButton()
        self.maximum_button = Gtk.SpinButton()
        for b in [self.minimum_button, self.edge_button, self.maximum_button]:
            b.set_numeric(True)
            b.set_snap_to_ticks(True)
            b.set_update_policy(Gtk.SpinButtonUpdatePolicy.IF_VALID)
        self.adjust(['minimum', 'edge', 'maximum'])
        self.minimum_button.set_value(Number(self.minimum))
        self.edge_button.set_value(Number(self.edge))
        self.maximum_button.set_value(Number(self.maximum))

        self.minimum_button.connect('value-changed', self.on_minimum_changed)
        self.edge_button.connect('value-changed', self.on_edge_changed)
        self.maximum_button.connect('value-changed', self.on_maximum_changed)

        steps_label = Gtk.Label(tr('Precision'))
        self.attach(steps_label, 0, 0, 1, 1)
        self.attach_next_to(self.steps_combo, steps_label,
                            Gtk.PositionType.RIGHT, 1, 1)

        mini_label = Gtk.Label(tr('Minimum'))
        self.attach_next_to(mini_label, steps_label,
                            Gtk.PositionType.BOTTOM, 1, 1)
        self.attach_next_to(self.minimum_button, mini_label,
                            Gtk.PositionType.RIGHT, 1, 1)

        edge_label = Gtk.Label(tr('Edge'))
        self.attach_next_to(edge_label, mini_label,
                            Gtk.PositionType.BOTTOM, 1, 1)
        self.attach_next_to(self.edge_button, edge_label,
                            Gtk.PositionType.RIGHT, 1, 1)

        maxi_label = Gtk.Label(tr('Maximum'))
        self.attach_next_to(maxi_label, edge_label,
                            Gtk.PositionType.BOTTOM, 1, 1)
        self.attach_next_to(self.maximum_button, maxi_label,
                            Gtk.PositionType.RIGHT, 1, 1)
        self.show_all()

    def on_steps_combo_changed(self, combo):
        self.step = Number(STEPS[int(combo.get_active_id())])
        self.adjust(['minimum', 'edge', 'maximum'])

    def on_minimum_changed(self, button):
        self.minimum = button.get_value()
        self.adjust(['edge', 'maximum'])

    def on_edge_changed(self, button):
        self.edge = button.get_value()
        self.adjust(['minimum', 'maximum'])

    def on_maximum_changed(self, button):
        self.maximum = button.get_value()
        self.adjust(['minimum', 'edge'])

    def adjust(self, buttons_list):
        for button_name in buttons_list:
            button = getattr(self, '{}_button'.format(button_name))
            button.set_digits(self.step.fracdigits_nb())
            button.set_increments(self.step, 10 * self.step)
            if button_name == 'minimum':
                button.set_range(0, Number(self.edge) - self.step)
            elif button_name == 'edge':
                button.set_range(Number(self.minimum) + self.step,
                                 Number(self.maximum) - self.step)
            elif button_name == 'maximum':
                button.set_range(Number(self.edge) + self.step,
                                 sys.maxsize)
