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

import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('GdkPixbuf', '2.0')
except ValueError:
    raise
else:
    from gi.repository import Gtk, Gio, GdkPixbuf


from cotinga.core.env import __myname__, __authors__, __version__
from cotinga.core.env import GUIDIR, COTINGA_ICON
from cotinga.core.env import LOCALEDIR, L10N_DOMAIN
from cotinga.core.shared import PREFS, STATUS
from .pupils_progression_manager import PupilsProgressionManagerPage
from .dialogs import PreferencesDialog


# TODO: add keyboard shorcuts
# examples: suppr to remove an entry (in any editable list),
# ctrl-O to open file, ctrl-s to save, ctrl-S to save as etc.

# TODO: add tooltips on buttons

class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
        super().__init__(*args, **kwargs)
        self.set_icon_from_file(COTINGA_ICON)
        self.set_border_width(3)

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = __myname__.capitalize()
        self.set_titlebar(hb)

        with open(os.path.join(GUIDIR, 'app_menu.xml'), 'r') as f:
            menu_xml = f.read()
        menu_xml = menu_xml.replace('LABEL_PREFERENCES', tr('Preferences'))
        menu_xml = menu_xml.replace('LABEL_ABOUT', tr('About'))
        menu_xml = menu_xml.replace('LABEL_QUIT', tr('Quit'))
        builder = Gtk.Builder.new_from_string(menu_xml, -1)
        menu = builder.get_object('app-menu')

        button = Gtk.MenuButton.new()
        popover = Gtk.Popover.new_from_model(button, menu)
        button.set_popover(popover)

        button.show()
        button = Gtk.MenuButton.new()
        icon = Gtk.Image.new_from_icon_name('open-menu-symbolic',
                                            Gtk.IconSize.BUTTON)
        button.add(icon)
        popover = Gtk.Popover.new_from_model(button, menu)

        button.set_popover(popover)
        hb.pack_end(button)

        self.notebook = Gtk.Notebook()
        self.pupils_progression_manager_page = PupilsProgressionManagerPage()
        # TODO: maybe move the set_sensitive() calls below to
        # PupilsProgressionManagerPage.__init__()
        self.pupils_progression_manager_page.toolbar\
            .buttons['document-save']\
            .set_sensitive(STATUS.document_modified)
        self.pupils_progression_manager_page.toolbar\
            .buttons['document-save-as']\
            .set_sensitive(STATUS.document_loaded)
        self.pupils_progression_manager_page.toolbar\
            .buttons['document-setup']\
            .set_sensitive(STATUS.document_loaded)
        self.pupils_progression_manager_page.toolbar\
            .buttons['document-close']\
            .set_sensitive(STATUS.document_loaded)
        self.notebook.append_page(self.pupils_progression_manager_page,
                                  Gtk.Label(''))
        self.refresh_progression_manager_tab_title()

        outergrid = Gtk.Grid()
        outergrid.add(self.notebook)
        outergrid.show()
        self.add(outergrid)
        self.app = kwargs.get('application')
        self.connect('delete-event', self.do_quit)

    def do_quit(self, *args):
        self.app.on_quit(None, None)

    def refresh_progression_manager_tab_title(self):
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
        title = tr('Progression manager')
        if STATUS.document_name:
            title = tr('Progression manager – {doc_title}')\
                .format(doc_title=os.path.basename(STATUS.document_name))
        elif STATUS.document_loaded:
            title = tr('Progression manager – (New document)')
        if STATUS.document_modified:
            title += ' *'
        self.notebook.set_tab_label(self.pupils_progression_manager_page,
                                    Gtk.Label(title))


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id='org.cotinga_app', **kwargs)
        self.window = None
        self.logo = GdkPixbuf.Pixbuf.new_from_file_at_scale(COTINGA_ICON,
                                                            128, -1, True)

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new('preferences', None)
        action.connect('activate', self.on_preferences)
        self.add_action(action)

        action = Gio.SimpleAction.new('about', None)
        action.connect('activate', self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new('quit', None)
        action.connect('activate', self.on_quit)
        self.add_action(action)

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = AppWindow(application=self,
                                    title=__myname__.capitalize())
        self.window.set_size_request(700, 350)
        self.window.set_default_size(800, 500)
        self.window.present()
        self.window.show_all()
        if self.window.pupils_progression_manager_page.view_panel is not None:
            self.window.pupils_progression_manager_page\
                .view_panel.setup_info_visibility()

    def on_preferences(self, action, param):
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
        pref_dialog = PreferencesDialog(tr('Preferences'), PREFS.language)
        pref_dialog.set_transient_for(self.window)
        pref_dialog.set_modal(True)
        pref_dialog.run()
        chosen_language = pref_dialog.chosen_language
        chosen_devtools = pref_dialog.devtools_switch.get_active()
        chosen_show_toolbar_labels = pref_dialog\
            .show_toolbar_labels_switch.get_active()
        pref_dialog.destroy()
        previous_language = PREFS.language
        previous_devtools = PREFS.enable_devtools
        previous_show_toolbar_labels = PREFS.show_toolbar_labels
        recreate_window = False
        if (chosen_language is not None
                and previous_language != chosen_language):
            PREFS.language = chosen_language
            recreate_window = True
        if previous_devtools != chosen_devtools:
            PREFS.enable_devtools = chosen_devtools
            recreate_window = True
        if previous_show_toolbar_labels != chosen_show_toolbar_labels:
            PREFS.show_toolbar_labels = chosen_show_toolbar_labels
            recreate_window = True
        if recreate_window:
            self.window.destroy()
            self.window = None
            self.do_activate()

    def on_about(self, action, param):
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
        about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
        about_dialog.set_authors(__authors__)
        about_dialog.set_version(__version__)
        about_dialog.set_program_name(__myname__)
        # about_dialog.props.wrap_license = True
        about_dialog.set_website(
            'https://gitlab.com/nicolas.hainaux/cotinga')
        about_dialog.set_website_label(tr('Cotinga website'))
        about_dialog.set_logo(self.logo)
        about_dialog.set_copyright('Copyright © 2018 Nicolas Hainaux')
        about_dialog.set_comments(tr('Cotinga helps teachers to manage '
                                     "their pupils' progression."))
        # with open('LICENSE', 'r') as f:  # Either this or the licence type
        #     about_dialog.set_license(f.read())
        about_dialog.set_license_type(Gtk.License.GPL_3_0)

        about_dialog.run()
        about_dialog.destroy()

    def on_quit(self, action, param):
        self.quit()
