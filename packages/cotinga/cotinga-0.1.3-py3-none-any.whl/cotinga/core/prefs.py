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
import sys
import locale
from shutil import copyfile
from gettext import translation

import toml

import gi
try:
    gi.require_version('Gtk', '3.0')
except ValueError:
    raise
else:
    from gi.repository import Gtk

from . import io
from .tools import ExtDict
from .env import LOCALEDIR
from .env import USER_PREFS_DIR, USER_COTINGA_PREFS_DIR, USER_PREFS_FILE
from .env import USER_PREFS_DEFAULT_FILE, USER_PREFS_LOCALIZED_DEFAULT_FILES
from .env import SUPPORTED_LANGUAGES, L10N_DOMAIN
from cotinga.gui.dialogs import PreferencesDialog

if sys.platform.startswith('win'):
    import ctypes
    FILE_ATTRIBUTE_HIDDEN = 0x02


def _firstrun_dialog():
    """Run when no ~/.config/cotinga/prefs.toml is found at start."""
    preferences = ExtDict()
    if not os.path.isdir(USER_PREFS_DIR):
        os.mkdir(USER_PREFS_DIR)
        if sys.platform.startswith('win'):
            ctypes.windll.kernel32.SetFileAttributesW(USER_PREFS_DIR,
                                                      FILE_ATTRIBUTE_HIDDEN)
    if not os.path.isdir(USER_COTINGA_PREFS_DIR):
        os.mkdir(USER_COTINGA_PREFS_DIR)
    copyfile(USER_PREFS_DEFAULT_FILE, USER_PREFS_FILE)
    window = Gtk.Window()
    try:
        language = locale.getdefaultlocale()[0]
        assert language in SUPPORTED_LANGUAGES
    except Exception:
        # We just want to guess the default locale, and check it
        # belongs to supported languages, so for any Exception
        # raised, we fall back to the default 'en_US' country code
        language = 'en_US'
    tr = translation(L10N_DOMAIN, LOCALEDIR, [language]).gettext
    pref_dialog = PreferencesDialog(
        tr('Cotinga - Preferences'), language, first_run=True, window=window)
    pref_dialog.run()
    chosen_language = pref_dialog.chosen_language \
        if pref_dialog.chosen_language is not None \
        else language
    preferences.recursive_update({'language': chosen_language})
    preferences.recursive_update(
        toml.load(USER_PREFS_LOCALIZED_DEFAULT_FILES[chosen_language]))
    save(preferences)
    pref_dialog.destroy()
    return preferences


def _from(filename, ioerror_handling=None):
    """
    Try to get preferences from filename.

    IOError handling is either ignored (if left to default None) or runs the
    first run dialog (if set to 'firstrun_dialog') to retrieve information.
    """
    preferences = ExtDict()
    try:
        with open(filename) as f:
            preferences = ExtDict(toml.load(f))
    except (IOError, FileNotFoundError):
        if ioerror_handling == 'firstrun_dialog':
            preferences = _firstrun_dialog()
    return preferences


def save(data):
    """Save the user prefs file updated with given data."""
    io.save(data, USER_PREFS_FILE)


def load():
    """Will load the values from the toml prefs file."""
    preferences = _from(USER_PREFS_DEFAULT_FILE)
    preferences.recursive_update(
        _from(USER_PREFS_FILE, ioerror_handling='firstrun_dialog'))
    return preferences
