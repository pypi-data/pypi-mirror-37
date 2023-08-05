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

from cotinga.core.env import LOCALEDIR, L10N_DOMAIN
from cotinga.core import shared, pmdoc
from cotinga.core.shared import PREFS
from cotinga.gui.panels import ListManagerPanel
from cotinga import gui
from cotinga.models import Pupils
from cotinga.data.default.data.pmdoc.presets import LEVELS_SCALES
from .pages import GradingManager

__all__ = ['DocumentSettingDialog']


class DocumentSettingDialog(Gtk.Dialog):

    def __init__(self):
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
        Gtk.Dialog.__init__(self, tr('Document settings'), gui.app.window, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_size_request(350, 200)
        self.box = self.get_content_area()
        self.grading_manager = GradingManager()
        docsetup = pmdoc.setting.load()
        self.levels_panel = \
            ListManagerPanel(docsetup['levels'], tr('Labels'),
                             presets=(LEVELS_SCALES(),
                                      tr('Load a preset scale'),
                                      tr('Replace current scale by: '),
                                      'document-import'))
        self.special_grades_panel = \
            ListManagerPanel(docsetup['special_grades'], tr('Labels'),
                             mini_items_nb=0)
        locked_classes = [
            classname
            for classname in docsetup['classes']
            if len(shared.session.query(Pupils)
                   .filter_by(classname=classname).all()) >= 1]
        self.classes_panel = \
            ListManagerPanel(docsetup['classes'], tr('Labels'),
                             mini_items_nb=0, locked=locked_classes)
        # From: https://lazka.github.io/pgi-docs/Gtk-3.0/classes/
        # Notebook.html#Gtk.Notebook.set_current_page
        # "it is recommended to show child widgets before adding them to a "
        # "notebook."
        # Hence it is not recommended to add pages first and use get_children()
        # to browse pages to show them...
        for page in [self.grading_manager, self.levels_panel,
                     self.special_grades_panel, self.classes_panel]:
            page.show()
        self.notebook = Gtk.Notebook()
        self.notebook.append_page(self.classes_panel,
                                  Gtk.Label(tr('Classes')))
        self.notebook.append_page(self.levels_panel,
                                  Gtk.Label(tr('Levels')))
        self.notebook.append_page(self.grading_manager,
                                  Gtk.Label(tr('Grading')))
        self.notebook.append_page(self.special_grades_panel,
                                  Gtk.Label(tr('Special grades')))
        self.notebook.set_current_page(0)
        self.box.add(self.notebook)
        self.show_all()
        self.from_page_num = self.notebook.get_current_page()
