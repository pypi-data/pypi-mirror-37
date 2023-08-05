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
    gi.require_version('EvinceView', '3.0')
    gi.require_version('EvinceDocument', '3.0')
except ValueError:
    raise
else:
    from gi.repository import Gtk, EvinceDocument, EvinceView

from cotinga import gui
from cotinga.core.env import REPORT_FILE_URI


__all__ = ['PreviewDialog']


class PreviewDialog(Gtk.Dialog):

    def __init__(self, title):
        Gtk.Dialog.__init__(self, title, gui.app.window, 0,
                            (Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE,
                             Gtk.STOCK_SAVE_AS, Gtk.ResponseType.YES,
                             Gtk.STOCK_PRINT, Gtk.ResponseType.OK))
        self.set_modal(True)

        self.set_size_request(480, 480)
        self.box = self.get_content_area()

        scroll = Gtk.ScrolledWindow()
        # self.add(scroll)
        EvinceDocument.init()
        doc = EvinceDocument.Document.factory_get_document(REPORT_FILE_URI)
        view = EvinceView.View()
        model = EvinceView.DocumentModel()
        model.set_document(doc)
        view.set_model(model)
        scroll.add(view)
        scroll.set_hexpand(True)
        scroll.set_vexpand(True)

        self.box.add(scroll)
        self.show_all()
