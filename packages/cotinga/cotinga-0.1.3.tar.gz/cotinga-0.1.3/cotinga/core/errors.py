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

from .env import LOCALEDIR, L10N_DOMAIN
from . import shared


class CotingaError(Exception):
    """Basic exception for errors raised by Cotinga."""
    def __init__(self, msg=None):
        PREFS = shared.PREFS
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
        if msg is None:
            msg = tr('An error occured in Cotinga')
        super().__init__(msg)


class FileError(CotingaError):
    """When a file cannot be loaded."""
    def __init__(self, filename, msg=None):
        PREFS = shared.PREFS
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
        if msg is None:
            msg = tr('Cannot load file: {filename}.')\
                .format(repr(filename))
        super().__init__(msg=msg)


class DuplicateContentError(CotingaError):
    """When finding a forbidden duplicate."""
    def __init__(self, content, msg=None):
        PREFS = shared.PREFS
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
        if msg is None:
            msg = tr('Duplicate content: {content}.')\
                .format(content=repr(content))
        super().__init__(msg=msg)


class EmptyContentError(CotingaError):
    """In case of forbidden empty content."""
    def __init__(self, msg=None):
        PREFS = shared.PREFS
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
        if msg is None:
            msg = tr('Empty content.')
        super().__init__(msg=msg)


class NoChangeError(CotingaError):
    """In case a change was expected."""
    def __init__(self, msg=None):
        PREFS = shared.PREFS
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
        if msg is None:
            msg = tr('No change.')
        super().__init__(msg=msg)


class ReservedCharsError(CotingaError):
    """When finding reserved characters."""
    def __init__(self, text, msg=None):
        PREFS = shared.PREFS
        tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
        if msg is None:
            msg = tr('Found reserved characters in: {text}.')\
                .format(text=repr(text))
        super().__init__(msg=msg)
