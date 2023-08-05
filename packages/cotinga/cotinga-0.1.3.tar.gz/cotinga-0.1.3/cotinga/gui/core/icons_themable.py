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

from abc import ABCMeta, abstractmethod

import gi
try:
    gi.require_version('Gtk', '3.0')
except ValueError:
    raise
else:
    from gi.repository import Gtk

from cotinga.core.env import ICON_THEME
from cotinga.core import shared

__all__ = ['IconsThemable']


class IconsThemable(object, metaclass=ABCMeta):

    def __init__(self):
        ICON_THEME.connect('changed', self.on_icon_theme_changed)

    def setup_buttons_icons(self, icon_theme):
        """Set icon and label of all buttons in self.buttons_icons()."""
        for btn_name in self.buttons_icons():
            for icon_name in self.buttons_icons()[btn_name]:
                if icon_theme.has_icon(icon_name):
                    button = getattr(self, btn_name)
                    if shared.PREFS.show_toolbar_labels:
                        btn_lbl_widget = Gtk.Grid()
                        pic = Gtk.Image.new_from_icon_name(
                            icon_name, Gtk.IconSize.LARGE_TOOLBAR)
                        btn_lbl_widget.attach(pic, 0, 0, 1, 1)
                        txt = self.buttons_labels()[btn_name]
                        lbl = Gtk.Label(txt)
                        lbl.props.margin_left = 5
                        btn_lbl_widget.attach_next_to(
                            lbl, pic, Gtk.PositionType.RIGHT, 1, 1)
                        button.set_label_widget(btn_lbl_widget)
                    else:
                        button.set_icon_name(icon_name)
                    break

    def on_icon_theme_changed(self, icon_theme):
        self.setup_buttons_icons(icon_theme)

    @abstractmethod
    def buttons_icons(self):
        """Defines icon names and fallback to standard icon name."""
        # Last item of each list is the fallback, hence must be standard

    @abstractmethod
    def buttons_labels(self):
        """Define labels of buttons."""
        # Must use the same names as in buttons_icons()
