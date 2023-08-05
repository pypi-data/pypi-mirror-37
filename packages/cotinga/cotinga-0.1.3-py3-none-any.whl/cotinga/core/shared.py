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

import toml

from . import status, prefs
from .pmdoc import database
from cotinga import gui
from .env import USER_PREFS_LOCALIZED_DEFAULT_FILES


class Status(object):

    def __init__(self):
        loaded_status = status.load()
        for key in loaded_status.keys():
            setattr(self, '_{}'.format(key), loaded_status[key])

    @property
    def document_loaded(self):
        return self._document_loaded

    @document_loaded.setter
    def document_loaded(self, value):
        # LATER: maybe check the value is boolean
        self._document_loaded = value
        gui.app.window\
            .pupils_progression_manager_page.toolbar\
            .buttons['document-setup']\
            .set_sensitive(value)
        gui.app.window\
            .pupils_progression_manager_page.toolbar\
            .buttons['document-close']\
            .set_sensitive(value)
        gui.app.window\
            .pupils_progression_manager_page.toolbar\
            .buttons['document-save-as']\
            .set_sensitive(value)
        gui.app.window\
            .pupils_progression_manager_page.setup_pages()
        status.save({'document_loaded': value})
        gui.app.window.refresh_progression_manager_tab_title()

    @property
    def document_modified(self):
        return self._document_modified

    @document_modified.setter
    def document_modified(self, value):
        # LATER: maybe check the value is boolean
        self._document_modified = value
        gui.app.window\
            .pupils_progression_manager_page.toolbar\
            .buttons['document-save']\
            .set_sensitive(value)
        status.save({'document_modified': value})
        gui.app.window.refresh_progression_manager_tab_title()

    @property
    def document_name(self):
        return self._document_name

    @document_name.setter
    def document_name(self, value):
        self._document_name = value
        status.save({'document_name': value})
        gui.app.window.refresh_progression_manager_tab_title()

    @property
    def filters(self):
        return self._filters

    @filters.setter
    def filters(self, value):
        self._filters = value
        status.save({'filters': value})

    @property
    def show_col_id(self):
        return self._show_col_id

    @show_col_id.setter
    def show_col_id(self, value):
        self._show_col_id = value
        status.save({'show_col_id': value})
        gui.app.window.pupils_progression_manager_page.refresh_visible_cols()

    @property
    def show_col_incl(self):
        return self._show_col_incl

    @show_col_incl.setter
    def show_col_incl(self, value):
        self._show_col_incl = value
        status.save({'show_col_incl': value})
        gui.app.window.pupils_progression_manager_page.refresh_visible_cols()

    @property
    def show_col_ilevel(self):
        return self._show_col_ilevel

    @show_col_ilevel.setter
    def show_col_ilevel(self, value):
        self._show_col_ilevel = value
        status.save({'show_col_ilevel': value})
        gui.app.window.pupils_progression_manager_page.refresh_visible_cols()


class Prefs(object):

    def __init__(self):
        loaded_prefs = prefs.load()
        self._language = loaded_prefs['language']
        self._pmreport = loaded_prefs['pmreport']
        self._enable_devtools = loaded_prefs['enable_devtools']
        self._show_toolbar_labels = loaded_prefs['show_toolbar_labels']

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, value):
        # We don't check the value (the only calls to set_language() must check
        # it belongs to SUPPORTED_LANGUAGES).
        self._language = value
        prefs.save({'language': value})
        # LATER: do this only at first run, then let the user handle this
        # (when he'll be able to define the date_fmt value on his own, in the
        # prefs dialog)
        prefs.save(toml.load(USER_PREFS_LOCALIZED_DEFAULT_FILES[value]))

    @property
    def pmreport(self):
        loaded_prefs = prefs.load()
        return loaded_prefs['pmreport']

    @property
    def enable_devtools(self):
        return self._enable_devtools

    @enable_devtools.setter
    def enable_devtools(self, value):
        self._enable_devtools = value
        prefs.save({'enable_devtools': value})

    @property
    def show_toolbar_labels(self):
        return self._show_toolbar_labels

    @show_toolbar_labels.setter
    def show_toolbar_labels(self, value):
        self._show_toolbar_labels = value
        prefs.save({'show_toolbar_labels': value})


def init():
    global STATUS, PREFS
    global engine, session, metadata

    STATUS = Status()
    PREFS = Prefs()

    engine = None
    session = None
    metadata = None

    if STATUS.document_loaded:
        database.load_session()
