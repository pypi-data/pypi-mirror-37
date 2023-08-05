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

import os
from gettext import translation

from babel import Locale
import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('GdkPixbuf', '2.0')
except ValueError:
    raise
else:
    from gi.repository import Gtk, GdkPixbuf

from cotinga import gui
from cotinga.core.env import L10N_DOMAIN, SUPPORTED_LANGUAGES
from cotinga.core.env import LOCALEDIR, FLAGSDIR
from cotinga.core import shared


__all__ = ['PreferencesDialog']


class PreferencesDialog(Gtk.Dialog):

    def __init__(self, title, default_language, first_run=False, window=None):
        # An optional window argument must be provided at first run
        if window is None:
            window = gui.app.window
        tr = translation(L10N_DOMAIN, LOCALEDIR, [default_language]).gettext
        buttons = {True: (Gtk.STOCK_OK, Gtk.ResponseType.OK),
                   False: (Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE)}
        Gtk.Dialog.__init__(self, title, window, 0, buttons[first_run])

        self.set_default_size(250, 100)
        self.box = self.get_content_area()
        self.main_grid = Gtk.Grid()
        self.main_grid.set_border_width(5)
        # As Gtk.Box will get deprecated, one can expect that
        # get_content_area() will later return something else than a Box.
        # Note that then, box can be replaced by self.main_grid

        self.main_grid.set_column_spacing(25)

        language_label = Gtk.Label(tr('Choose a language:'))
        self.main_grid.attach(language_label, 0, 0, 1, 1)

        store = Gtk.ListStore(GdkPixbuf.Pixbuf, str)
        self.languages = {}
        currently_selected = -1
        for i, lang_code in enumerate(SUPPORTED_LANGUAGES):
            loc = Locale.parse(lang_code)
            language_name = loc.get_display_name(default_language)
            flag_filename = '{}.svg'.format(lang_code.split('_')[1])
            flag_icon = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                os.path.join(FLAGSDIR, flag_filename), 24, -1, True)
            store.append([flag_icon, language_name])
            self.languages[language_name] = lang_code
            if lang_code == default_language:
                currently_selected = i

        combo = Gtk.ComboBox.new_with_model(store)

        renderer = Gtk.CellRendererPixbuf()
        combo.pack_start(renderer, True)
        combo.add_attribute(renderer, 'pixbuf', 0)

        renderer = Gtk.CellRendererText()
        combo.pack_start(renderer, False)
        combo.add_attribute(renderer, 'text', 1)

        if currently_selected >= 0:
            combo.set_active(currently_selected)
        combo.connect('changed', self.on_language_changed)

        self.chosen_language = None

        self.main_grid.attach_next_to(combo, language_label,
                                      Gtk.PositionType.BOTTOM, 1, 1)

        if not first_run:
            show_toolbar_labels = Gtk.Label(tr('Show toolbar buttons labels'))
            show_toolbar_labels.props.margin_right = 10
            self.show_toolbar_labels_switch = Gtk.Switch()
            self.show_toolbar_labels_switch.set_active(
                shared.PREFS.show_toolbar_labels)

            self.main_grid.attach_next_to(show_toolbar_labels, language_label,
                                          Gtk.PositionType.RIGHT, 1, 1)
            self.main_grid.attach_next_to(self.show_toolbar_labels_switch,
                                          combo,
                                          Gtk.PositionType.RIGHT, 1, 1)

            devtools_label = Gtk.Label(tr('Developer tools'))
            devtools_label.props.margin_right = 10
            self.devtools_switch = Gtk.Switch()
            self.devtools_switch.set_active(shared.PREFS.enable_devtools)

            self.main_grid.attach_next_to(devtools_label, show_toolbar_labels,
                                          Gtk.PositionType.RIGHT, 1, 1)
            self.main_grid.attach_next_to(self.devtools_switch,
                                          self.show_toolbar_labels_switch,
                                          Gtk.PositionType.RIGHT, 1, 1)

        self.box.add(self.main_grid)
        self.show_all()

    def on_language_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            language_name = model[tree_iter][1]
            print('Selected: language_name={}, country_code={}'
                  .format(language_name, self.languages[language_name]))
            self.chosen_language = self.languages[language_name]
        else:
            entry = combo.get_child()
            print('Entered: %s' % entry.get_text())
