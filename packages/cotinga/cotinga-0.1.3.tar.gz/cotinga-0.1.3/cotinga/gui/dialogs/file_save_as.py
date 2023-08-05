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

from datetime import datetime
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
from cotinga.core.tools import add_cot_filters, add_pdf_filters

__all__ = ['SaveAsFileDialog']


class SaveAsFileDialog(Gtk.FileChooserDialog):

    def __init__(self, report=False):
        """
        :param report: whether we're about to save a report rather than the
        current user file
        :type report: bool
        """
        PREFS = shared.PREFS
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
        Gtk.FileChooserDialog.__init__(self, tr('Please choose a file'),
                                       gui.app.window,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE_AS,
                                        Gtk.ResponseType.OK))
        if report:
            date_fmt = shared.PREFS.pmreport['date_fmt']
            date = datetime.now().strftime(date_fmt).replace('/', '-')
            self.set_current_name(tr('Report {date}.pdf')
                                  .format(date=date))
        else:
            if shared.STATUS.document_name == '':
                self.set_current_name(tr('Untitled.tgz'))
            else:
                self.set_filename(shared.STATUS.document_name)
        self.set_modal(True)
        self.set_do_overwrite_confirmation(True)
        if report:
            add_pdf_filters(self)
        else:
            add_cot_filters(self)
