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
from cotinga.gui.core import IconsThemable
from cotinga.core import shared
from cotinga.core.env import ICON_THEME, L10N_DOMAIN, LOCALEDIR
from cotinga.core import pmdoc
from .dialogs import DocumentSettingDialog

document = pmdoc.document


class __MetaThemableToolbar(type(Gtk.Toolbar), type(IconsThemable)):
    pass


class PupilsProgressionManagerToolbar(Gtk.Toolbar, IconsThemable,
                                      metaclass=__MetaThemableToolbar):

    def __init__(self):
        Gtk.Toolbar.__init__(self)
        IconsThemable.__init__(self)

        self.doc_new_button = Gtk.ToolButton.new()
        self.doc_new_button.set_vexpand(False)
        self.doc_new_button.set_halign(Gtk.Align.CENTER)
        self.doc_new_button.set_valign(Gtk.Align.CENTER)
        self.doc_new_button.connect('clicked', self.on_doc_new_clicked)
        self.add(self.doc_new_button)

        self.doc_open_button = Gtk.ToolButton.new()
        self.doc_open_button.set_vexpand(False)
        self.doc_open_button.set_halign(Gtk.Align.CENTER)
        self.doc_open_button.set_valign(Gtk.Align.CENTER)
        self.doc_open_button.connect('clicked', self.on_doc_open_clicked)
        self.add(self.doc_open_button)

        self.doc_save_button = Gtk.ToolButton.new()
        self.doc_save_button.set_vexpand(False)
        self.doc_save_button.set_halign(Gtk.Align.CENTER)
        self.doc_save_button.set_valign(Gtk.Align.CENTER)
        self.doc_save_button.connect('clicked', self.on_doc_save_clicked)
        self.add(self.doc_save_button)

        self.doc_save_as_button = Gtk.ToolButton.new()
        self.doc_save_as_button.props.icon_name = 'document-save-as'
        self.doc_save_as_button.set_vexpand(False)
        self.doc_save_as_button.set_halign(Gtk.Align.CENTER)
        self.doc_save_as_button.set_valign(Gtk.Align.CENTER)
        self.doc_save_as_button.connect('clicked', self.on_doc_save_as_clicked)
        self.add(self.doc_save_as_button)

        self.doc_close_button = Gtk.ToolButton.new()
        self.doc_close_button.set_vexpand(False)
        self.doc_close_button.set_halign(Gtk.Align.CENTER)
        self.doc_close_button.set_valign(Gtk.Align.CENTER)
        self.doc_close_button.connect('clicked', self.on_doc_close_clicked)
        self.add(self.doc_close_button)

        self.doc_setting_button = Gtk.ToolButton.new()
        self.doc_setting_button.set_vexpand(False)
        self.doc_setting_button.set_halign(Gtk.Align.CENTER)
        self.doc_setting_button.set_valign(Gtk.Align.CENTER)
        self.doc_setting_button.connect(
            'clicked', self.on_doc_setting_clicked)
        self.add(self.doc_setting_button)

        # LATER: add a document-open-recent button

        self.buttons = {'document-new': self.doc_new_button,
                        'document-open': self.doc_open_button,
                        'document-close': self.doc_close_button,
                        'document-save': self.doc_save_button,
                        'document-save-as': self.doc_save_as_button,
                        'document-setup': self.doc_setting_button}
        self.setup_buttons_icons(ICON_THEME)

    def buttons_icons(self):
        """Define icon names and fallback to standard icon name."""
        # Last item of each list is the fallback, hence must be standard
        buttons = {'doc_new_button': ['document-new'],
                   'doc_open_button': ['document-open'],
                   'doc_save_button': ['document-save'],
                   'doc_save_as_button': ['document-save-as'],
                   'doc_close_button': ['document-close', 'window-close'],
                   'doc_setting_button': ['gnome-settings',
                                          'preferences-desktop'],
                   }
        return buttons

    def buttons_labels(self):
        """Define labels of buttons."""
        PREFS = shared.PREFS
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
        buttons = {'doc_new_button': tr('New'),
                   'doc_open_button': tr('Open'),
                   'doc_save_button': tr('Save'),
                   'doc_save_as_button': tr('Save as...'),
                   'doc_close_button': tr('Close'),
                   'doc_setting_button': tr('Settings'),
                   }
        return buttons

    def on_doc_new_clicked(self, widget):
        """Called on "new file" clicks"""
        document.new()

    def on_doc_close_clicked(self, widget):
        """Called on "close file" clicks"""
        document.close()

    def on_doc_save_as_clicked(self, widget):
        """Called on "save as" clicks"""
        document.save_as()

    def on_doc_save_clicked(self, widget):
        """Called on "save as" clicks"""
        document.save()

    def on_doc_open_clicked(self, widget):
        """Called on "open file" clicks"""
        document.open_()

    def on_doc_setting_clicked(self, widget):
        """Called on "document setup" clicks"""
        dialog = DocumentSettingDialog()
        dialog.set_modal(True)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            # LATER: when validating, if the user is inserting something that
            # he did not validate yet via return, then it's lost. Check if
            # there's a way to keep the entry if it's not
            # None (e.g. validate it or not via cell_edited().
            # The 'editing-canceled' event from CellRendererText seems useless
            # unfortunately (the text is then already set to None)
            # Maybe a way is to disable the validate button when insert_button
            # is clicked and until the entry is validated by return.
            new_levels = [row[0] for row in dialog.levels_panel.store
                          if row[0] is not None]
            new_special_grades = [row[0]
                                  for row in dialog.special_grades_panel.store
                                  if row[0] is not None]
            new_grading = dialog.grading_manager.get_grading()
            new_classes = [row[0]
                           for row in dialog.classes_panel.store
                           if row[0] is not None]
            docsetup = pmdoc.setting.load()
            previous_levels = docsetup['levels']
            previous_special_grades = docsetup['special_grades']
            previous_grading = docsetup['grading']
            previous_classes = docsetup['classes']
            if new_classes != previous_classes:
                # Remove filters of removed classes from filters ON, if any
                shared.STATUS.filters = [label
                                         for label in shared.STATUS.filters
                                         if label in new_classes]
            if any(new != previous
                   for (new, previous) in zip([new_levels,
                                               new_special_grades,
                                               new_grading,
                                               new_classes],
                                              [previous_levels,
                                               previous_special_grades,
                                               previous_grading,
                                               previous_classes])):
                docsetup = pmdoc.setting.save(
                    {'levels': new_levels,
                     'special_grades': new_special_grades,
                     'classes': new_classes,
                     'grading': new_grading})
                shared.STATUS.document_modified = True
                gui.app.window.pupils_progression_manager_page.setup_pages()
        dialog.destroy()
