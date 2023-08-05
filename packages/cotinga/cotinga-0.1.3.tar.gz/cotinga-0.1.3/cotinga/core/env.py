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
from pathlib import Path

import gi
try:
    gi.require_version('Gtk', '3.0')
except ValueError:
    raise
else:
    from gi.repository import Gtk

import toml


__process_name = os.path.basename(__file__)
__abspath = os.path.abspath(__file__)
__l1 = len(__process_name)
__l2 = len(__abspath)
CORE_DIRNAME = 'core/'
ROOTDIR = __abspath[:__l2 - __l1][:-(len(CORE_DIRNAME) + 1)]
DATADIR = os.path.join(ROOTDIR, 'data')

with open(os.path.join(DATADIR, 'metadata.toml'), 'r') as f:
    pp = toml.load(f)

__myname__ = pp['__myname__']
__authors__ = pp['__authors__']
__version__ = pp['__version__']

DATARUNDIR = os.path.join(DATADIR, 'run')
CONFIGDIR = os.path.join(DATADIR, 'default/')
LOCALEDIR = os.path.join(DATADIR, 'locale/')
GUIDIR = os.path.join(ROOTDIR, 'gui/')
STYLEDIR = os.path.join(DATADIR, 'style/')
PICSDIR = os.path.join(DATADIR, 'pics/')
FLAGSDIR = os.path.join(PICSDIR, 'flags/')
DEFAULTDATAPREFSDIR = os.path.join(CONFIGDIR, 'data', 'prefs')
COTINGA_ICON = os.path.join(PICSDIR, 'cotinga_icon.svg')
COTINGA_FADED_ICON = os.path.join(PICSDIR, 'cotinga_icon_faded.svg')
COTINGA_BW_ICON = os.path.join(PICSDIR, 'cotinga_icon_black_and_white.svg')
COTINGA_FADED_BW_ICON = os.path.join(PICSDIR,
                                     'cotinga_icon_faded_black_and_white.svg')

# PMDOC stands for Progression Manager DOCument
PMDOC_DB_FILENAME = 'pupils.db'
PMDOC_DB_MIMETYPE = 'application/x-sqlite3'
PMDOC_DB_URI = 'sqlite:///{}/data/run/pmdoc/{}'\
    .format(ROOTDIR, PMDOC_DB_FILENAME)

PMDOC_DIR = os.path.join(DATADIR, 'run/pmdoc')
PMDEFAULTSDIR = os.path.join(DATADIR, 'default/files/pmdocsettings')
PMDOC_DB_PATH = os.path.join(PMDOC_DIR, PMDOC_DB_FILENAME)
PMDOC_SETUP_FILENAME = 'setting.toml'
PMDOC_SETUP_MIMETYPE = 'text/plain'
PMDOC_SETUP_PATH = os.path.join(PMDOC_DIR, PMDOC_SETUP_FILENAME)

RUN_DB_FILE = os.path.join(DATARUNDIR, PMDOC_DB_FILENAME)
RUN_SETUP_FILE = os.path.join(DATARUNDIR, PMDOC_SETUP_FILENAME)

CFG_EXTENSION = '.toml'
USER_PREFS_DIR = os.path.join(str(Path.home()), '.config')
USER_COTINGA_PREFS_DIR = os.path.join(USER_PREFS_DIR, __myname__)
USER_PREFS_FILE = os.path.join(USER_COTINGA_PREFS_DIR,
                               'prefs' + CFG_EXTENSION)
USER_PREFS_DEFAULT_FILE = os.path.join(CONFIGDIR, 'files',
                                       'prefs' + CFG_EXTENSION)

STATUS_FILE = os.path.join(DATARUNDIR, 'status' + CFG_EXTENSION)
DEFAULT_STATUS_FILE = os.path.join(CONFIGDIR, 'files',
                                   'status' + CFG_EXTENSION)

REPORT_FILE = os.path.join(DATARUNDIR, 'report.pdf')
REPORT_FILE_URI = 'file://{}'.format(REPORT_FILE)

L10N_DOMAIN = __myname__
LOCALES = \
    {'en_US': 'en-US' if sys.platform.startswith('win') else 'en_US.UTF-8',
     'fr_FR': 'fr-FR' if sys.platform.startswith('win') else 'fr_FR.UTF-8'}
SUPPORTED_LANGUAGES = list(LOCALES.keys())

PMDEFAULTS_FILES = {k: os.path.join(PMDEFAULTSDIR, '{}.toml'.format(k))
                    for k in list(LOCALES.keys())}

USER_PREFS_LOCALIZED_DEFAULT_FILES = \
    {k: os.path.join(DEFAULTDATAPREFSDIR, '{}.toml'.format(k))
     for k in list(LOCALES.keys())}

ICON_THEME = Gtk.IconTheme.get_default()


def get_theme_name():
    return Gtk.Settings.get_default().props.gtk_theme_name


def get_icon_theme_name():
    return Gtk.Settings.get_default().props.gtk_icon_theme_name


def get_theme_provider(name=None):
    if name is None:
        name = get_theme_name()
    return Gtk.CssProvider.get_named(name, None)


THEME_STYLE_CONTEXT = Gtk.StyleContext.new()


def get_theme_colors():
    THEME_STYLE_CONTEXT.add_provider(get_theme_provider(),
                                     Gtk.STYLE_PROVIDER_PRIORITY_FALLBACK)
    _, fg_color = THEME_STYLE_CONTEXT.lookup_color('fg_color')
    _, bg_color = THEME_STYLE_CONTEXT.lookup_color('bg_color')
    _, sel_fg_color = THEME_STYLE_CONTEXT.lookup_color('selected_fg_color')
    _, sel_bg_color = THEME_STYLE_CONTEXT.lookup_color('selected_bg_color')

    return (fg_color, bg_color, sel_fg_color, sel_bg_color)


def convert_gdk_rgba_to_hex(color):
    """
    Converts Gdk.RGBA to hexadecimal value.

    :param color: the Gdk.RGBA object to convert
    :type color: gi.overrides.Gdk.RGBA
    """
    return '#{}{}{}{}'\
        .format(hex(int(255 * color.red)).replace('0x', ''),
                hex(int(255 * color.green)).replace('0x', ''),
                hex(int(255 * color.blue)).replace('0x', ''),
                hex(int(255 * color.alpha)).replace('0x', ''))
