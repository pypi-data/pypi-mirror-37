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

from cotinga import gui


def run_message_dialog(title, info, icon_name, parent=None):
    if parent is None:
        parent = gui.app.window
    dialog = Gtk.Dialog(title, parent,
                        0, (Gtk.STOCK_OK, Gtk.ResponseType.OK),
                        modal=True)
    dialog.set_default_size(150, 100)
    label = Gtk.Label(info)
    # REVIEW: Dialog icon set is ignored (bug?)
    # dialog.set_icon(
    #     Gtk.Image.new_from_icon_name('dialog-information',
    #                                  Gtk.IconSize.BUTTON)
    #     .get_pixbuf())
    bigger_icon = Gtk.Image.new_from_icon_name(
        icon_name, Gtk.IconSize.DIALOG)
    grid = Gtk.Grid()
    grid.attach(bigger_icon, 0, 0, 1, 1)
    grid.attach_next_to(label, bigger_icon,
                        Gtk.PositionType.RIGHT, 1, 1)
    box = dialog.get_content_area()
    box.add(grid)
    dialog.show_all()
    dialog.run()
    dialog.destroy()
