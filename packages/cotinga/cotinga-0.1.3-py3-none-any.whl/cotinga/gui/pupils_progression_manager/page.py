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
    gi.require_version('GdkPixbuf', '2.0')
except ValueError:
    raise
else:
    from gi.repository import Gtk, GdkPixbuf

from cotinga.core import shared, pmdoc
from cotinga.gui.panels import PupilsManagerPanel, PupilsViewPanel
from .toolbar import PupilsProgressionManagerToolbar
from cotinga.core.env import LOCALEDIR, L10N_DOMAIN, COTINGA_FADED_ICON
from cotinga.core.env import __version__


class PupilsProgressionManagerPage(Gtk.Grid):

    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_border_width(3)

        self.toolbar = PupilsProgressionManagerToolbar()
        self.toolbar.set_margin_top(6)
        self.attach(self.toolbar, 0, 0, 1, 1)

        self.classnames = None
        self.panels = {}
        self.classes_stack = None
        self.stack_switcher = None
        self.main_grid = None
        self.view_panel = None

        self.setup_pages()

    def new_switch_and_stack(self):
        PREFS = shared.PREFS
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
        if self.classes_stack is not None:
            self.classes_stack.destroy()
        self.classes_stack = Gtk.Stack()
        self.classes_stack.set_transition_type(Gtk.StackTransitionType.NONE)
        self.classes_stack.set_transition_duration(300)
        if self.stack_switcher is not None:
            self.stack_switcher.destroy()
        self.stack_switcher = Gtk.StackSwitcher()
        self.stack_switcher.props.margin_bottom = 10
        self.stack_switcher.props.margin_top = 10
        self.stack_switcher.set_stack(self.classes_stack)
        self.main_grid.attach(self.stack_switcher, 0, 0, 1, 1)

        self.view_cols_buttons = Gtk.Grid()
        self.view_cols_buttons.set_vexpand(False)
        self.view_cols_buttons.set_halign(Gtk.Align.END)
        self.view_cols_buttons.set_valign(Gtk.Align.END)
        self.view_cols_buttons.props.margin_right = 3
        view_cols_label = Gtk.Label(tr('View columns:'))
        view_cols_label.props.margin_right = 10
        self.view_cols_buttons.attach(view_cols_label, 0, 0, 1, 1)

        self.view_id_btn = Gtk.CheckButton('id')
        self.view_id_btn.set_active(shared.STATUS.show_col_id)
        self.view_id_btn.connect('toggled', self.on_view_id_toggled)

        self.view_incl_btn = Gtk.CheckButton(tr('Included'))
        self.view_incl_btn.set_active(shared.STATUS.show_col_incl)
        self.view_incl_btn.connect('toggled', self.on_view_incl_toggled)

        self.view_ilevel_btn = Gtk.CheckButton(tr('Initial level'))
        self.view_ilevel_btn.set_active(shared.STATUS.show_col_ilevel)
        self.view_ilevel_btn.connect('toggled', self.on_view_ilevel_toggled)

        if PREFS.enable_devtools:
            items = [view_cols_label, self.view_id_btn, self.view_incl_btn,
                     self.view_ilevel_btn]
        else:
            items = [view_cols_label, self.view_incl_btn, self.view_ilevel_btn]
        for i, item in enumerate(items):
            if i:
                self.view_cols_buttons.attach_next_to(
                    item, items[i - 1], Gtk.PositionType.RIGHT, 1, 1)

        self.main_grid.attach_next_to(
            self.view_cols_buttons, self.stack_switcher,
            Gtk.PositionType.BOTTOM, 1, 1)
        self.main_grid.attach_next_to(self.classes_stack, self.stack_switcher,
                                      Gtk.PositionType.BOTTOM, 1, 1)

    def setup_pages(self):
        PREFS = shared.PREFS
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
        if self.main_grid is not None:
            self.main_grid.destroy()
        self.main_grid = Gtk.Grid()
        self.attach_next_to(self.main_grid, self.toolbar,
                            Gtk.PositionType.BOTTOM, 1, 1)
        if shared.session is None:
            cot_icon = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                COTINGA_FADED_ICON, 128, -1, True)
            cot_icon = Gtk.Image.new_from_pixbuf(cot_icon)
            # TODO: write the welcome line bigger and bold (Pango)
            welcome_label = Gtk.Label(tr('Welcome in Cotinga'))
            # TODO: write the version line smaller and faded (Pango)
            version_label = Gtk.Label(tr('Version {}').format(__version__))
            version_label.props.margin_bottom = 15
            icon1 = Gtk.Image.new_from_icon_name('document-new',
                                                 Gtk.IconSize.DIALOG)
            icon1.props.margin = 10
            icon2 = Gtk.Image.new_from_icon_name('document-open',
                                                 Gtk.IconSize.DIALOG)
            icon2.props.margin = 10
            label = Gtk.Label(tr('You can create a new document\nor '
                                 'load an existing one.'))
            inner_grid = Gtk.Grid()
            inner_grid.set_vexpand(True)
            inner_grid.set_hexpand(True)
            inner_grid.set_halign(Gtk.Align.CENTER)
            inner_grid.set_valign(Gtk.Align.CENTER)
            inner_grid.attach(cot_icon, 0, 0, 3, 1)
            inner_grid.attach_next_to(welcome_label, cot_icon,
                                      Gtk.PositionType.BOTTOM, 3, 1)
            inner_grid.attach_next_to(version_label, welcome_label,
                                      Gtk.PositionType.BOTTOM, 3, 1)
            inner_grid.attach_next_to(icon1, version_label,
                                      Gtk.PositionType.BOTTOM, 1, 1)
            inner_grid.attach_next_to(icon2, icon1,
                                      Gtk.PositionType.RIGHT, 1, 1)
            inner_grid.attach_next_to(label, icon2,
                                      Gtk.PositionType.RIGHT, 1, 1)
            inner_grid.show_all()
            self.main_grid.attach(inner_grid, 0, 0, 1, 1)

        else:
            classnames = pmdoc.setting.load()['classes']
            if classnames:
                self.panels = {}
                self.classnames = classnames
                self.new_switch_and_stack()
                if self.view_panel is not None:
                    self.view_panel.destroy()
                self.view_panel = PupilsViewPanel()
                self.classes_stack.add_titled(self.view_panel,
                                              'pupils_view_panel',
                                              tr('Global view'))
                for label in classnames:
                    panel = PupilsManagerPanel(label)
                    panel.connect('data_changed', self.on_data_changed)
                    self.classes_stack.add_titled(panel, label, label)
                    self.panels[label] = panel
            else:
                icon = Gtk.Image.new_from_icon_name('gnome-settings',
                                                    Gtk.IconSize.DIALOG)
                icon.props.margin = 10
                label = Gtk.Label(tr('You can start creating classes in the '
                                     'document settings.'))
                inner_grid = Gtk.Grid()
                inner_grid.set_vexpand(True)
                inner_grid.set_hexpand(True)
                inner_grid.set_halign(Gtk.Align.CENTER)
                inner_grid.set_valign(Gtk.Align.CENTER)
                inner_grid.attach(icon, 0, 0, 1, 1)
                inner_grid.attach_next_to(label, icon,
                                          Gtk.PositionType.RIGHT, 1, 1)
                inner_grid.show_all()
                self.main_grid.attach(inner_grid, 0, 0, 1, 1)
        self.show_all()
        if self.view_panel is not None:
            self.view_panel.setup_info_visibility()

    def on_data_changed(self, *args):
        self.view_panel.refresh()

    def on_view_id_toggled(self, *args):
        shared.STATUS.show_col_id = not shared.STATUS.show_col_id

    def on_view_incl_toggled(self, *args):
        shared.STATUS.show_col_incl = not shared.STATUS.show_col_incl

    def on_view_ilevel_toggled(self, *args):
        shared.STATUS.show_col_ilevel = not shared.STATUS.show_col_ilevel

    def refresh_visible_cols(self, *args):
        panels = [self.panels[p] for p in self.panels] + [self.view_panel]
        for p in panels:
            p.col_id.set_visible(shared.STATUS.show_col_id
                                 and shared.PREFS.enable_devtools)
            p.col_incl.set_visible(shared.STATUS.show_col_incl)
            p.col_ilevel.set_visible(shared.STATUS.show_col_ilevel)
