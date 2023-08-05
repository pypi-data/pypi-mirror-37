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

import gi
try:
    gi.require_version('Gtk', '3.0')
except ValueError:
    raise
else:
    from gi.repository import Gtk

from cotinga import gui
from cotinga.core import shared
from cotinga.core.env import L10N_DOMAIN, LOCALEDIR

__all__ = ['SaveBeforeDialog']


class SaveBeforeDialog(Gtk.Dialog):

    def __init__(self, message):
        PREFS = shared.PREFS
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
        Gtk.Dialog.__init__(self, tr('Unsaved document'), gui.app.window, 0,
                            (Gtk.STOCK_YES, Gtk.ResponseType.YES,
                             Gtk.STOCK_NO, Gtk.ResponseType.NO,
                             Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        self.set_modal(True)

        self.set_size_request(450, 100)
        self.box = self.get_content_area()
        self.main_grid = Gtk.Grid()
        self.main_grid.set_border_width(5)
        self.main_grid.set_hexpand(True)
        # As Gtk.Box will get deprecated, one can expect that
        # get_content_area() will later return something else than a Box.
        # Note that then, box can be replaced by self.main_grid
        icon = Gtk.Image.new_from_icon_name('dialog-question',
                                            Gtk.IconSize.DIALOG)
        self.main_grid.attach(icon, 0, 0, 1, 1)
        message_label = Gtk.Label(message)
        self.main_grid.attach_next_to(message_label, icon,
                                      Gtk.PositionType.RIGHT, 1, 1)

        self.box.add(self.main_grid)
        self.show_all()
