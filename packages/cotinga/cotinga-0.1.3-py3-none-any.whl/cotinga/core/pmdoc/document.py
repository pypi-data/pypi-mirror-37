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
import tarfile
from tarfile import ReadError, CompressionError
from shutil import move, copyfile
from gettext import translation

import magic
import gi
try:
    gi.require_version('Gtk', '3.0')
except ValueError:
    raise
else:
    from gi.repository import Gtk

from cotinga.gui.dialogs import run_message_dialog, OpenFileDialog
from cotinga.gui.dialogs import SaveAsFileDialog, SaveBeforeDialog
from . import database, setting
from .. import shared
from ..env import LOCALEDIR, L10N_DOMAIN
from ..env import DATARUNDIR, RUN_DB_FILE
from ..env import RUN_SETUP_FILE
from ..env import PMDOC_DB_PATH, PMDOC_SETUP_PATH, PMDOC_DIR
from ..env import PMDOC_DB_FILENAME, PMDOC_DB_MIMETYPE, PMDOC_SETUP_MIMETYPE
from ..env import PMDOC_SETUP_FILENAME
from ..env import PMDEFAULTS_FILES
from ..env import __myname__
from ..errors import FileError
from ..tools import is_cot_file

TAR_LISTING = {PMDOC_DB_FILENAME, PMDOC_SETUP_FILENAME}


def new():
    """Create and load a new empty document."""
    tr = translation(L10N_DOMAIN, LOCALEDIR, [shared.PREFS.language]).gettext
    cancel = save_before(tr('Save current document before creating a new '
                            'one?'))
    if not cancel:
        database.terminate_session()

        copyfile(PMDEFAULTS_FILES[shared.PREFS.language], PMDOC_SETUP_PATH)
        database.load_session(init=True)  # Also creates a new pupils.db

        shared.STATUS.document_loaded = True
        shared.STATUS.document_modified = False
        shared.STATUS.document_name = ''
        shared.STATUS.filters = []


def close():
    """Close the current document."""
    tr = translation(L10N_DOMAIN, LOCALEDIR, [shared.PREFS.language]).gettext
    cancel = save_before(tr('Save current document before closing it?'))
    if not cancel:
        database.terminate_session()
        if os.path.isfile(PMDOC_SETUP_PATH):
            os.remove(PMDOC_SETUP_PATH)

        shared.STATUS.document_loaded = False
        shared.STATUS.document_modified = False
        shared.STATUS.document_name = ''
        shared.STATUS.filters = []


def __copy_document_to(dest):
    with tarfile.open(dest, 'w:gz') as tar:
        files_to_add = [os.path.join(PMDOC_DIR, f)
                        for f in os.listdir(PMDOC_DIR)
                        if f in TAR_LISTING]
        for f in files_to_add:
            tar.add(f, arcname=os.path.basename(f))


def save():
    """Save the current document without changing the file name."""
    cancel = False
    if shared.STATUS.document_name == '':
        cancel = save_as()
    else:
        __copy_document_to(shared.STATUS.document_name)
        shared.STATUS.document_modified = False
    return cancel


def save_as():
    """Save the current document with a new name."""
    cancel = False
    dialog = SaveAsFileDialog()
    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        doc_name = dialog.get_filename()
        if not doc_name.endswith('.tgz'):
            doc_name += '.tgz'
        shared.STATUS.document_name = doc_name
        __copy_document_to(shared.STATUS.document_name)
        shared.STATUS.document_modified = False
    elif response == Gtk.ResponseType.CANCEL:
        cancel = True
    dialog.destroy()
    return cancel


def save_before(message):
    """
    If document is modified, ask if it should be saved.

    Return True if the current action should be cancelled instead.

    :param message: a string to specify the reason of the action
    :type message: str
    :rtype: bool
    """
    cancel = False
    if shared.STATUS.document_modified:
        dialog = SaveBeforeDialog(message)
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            cancel = save()
        elif response == Gtk.ResponseType.CANCEL:
            cancel = True
    return cancel


def check_file(doc_name):
    PREFS = shared.PREFS
    tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
    if not is_cot_file(doc_name):
        raise FileError(doc_name, msg=tr('This file is not a readable '
                                         'compressed archive.'))
    try:
        with tarfile.open(doc_name, mode='r:gz') as archive:
            if set(archive.getnames()) != TAR_LISTING:
                raise FileError(doc_name,
                                msg=tr('This archive file does not contain '
                                       'the expected parts (found {}).')
                                .format(archive.getnames()))
            archive.extractall(path=DATARUNDIR)
            db_mimetype_found = \
                magic.detect_from_filename(RUN_DB_FILE).mime_type
            if db_mimetype_found != PMDOC_DB_MIMETYPE:
                raise FileError(doc_name,
                                msg=tr('The database is not correct '
                                       '(found MIME type {}).')
                                .format(db_mimetype_found))
            setup_mimetype_found = \
                magic.detect_from_filename(RUN_SETUP_FILE).mime_type
            if setup_mimetype_found != PMDOC_SETUP_MIMETYPE:
                raise FileError(doc_name,
                                msg=tr('The setup part is not correct '
                                       '(found MIME type {}).')
                                .format(setup_mimetype_found))
            database.check_db(RUN_DB_FILE)
    except (ReadError, CompressionError):
        raise FileError(doc_name,
                        msg=tr('This file could not be read or uncompressed '
                               'correctly.'))


def open_():
    tr = translation(L10N_DOMAIN, LOCALEDIR, [shared.PREFS.language]).gettext
    cancel = save_before(tr('Save current document before opening another '
                            'one?'))
    if not cancel:
        dialog = OpenFileDialog()
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            doc_name = dialog.get_filename()
            try:
                check_file(doc_name)
            except FileError as excinfo:
                tr = translation(L10N_DOMAIN, LOCALEDIR,
                                 [shared.PREFS.language]).gettext
                run_message_dialog(
                    tr('Cannot load file'),
                    tr('{software_name} cannot use this file.\n'
                       'Details: {details}')
                    .format(software_name=__myname__.capitalize(),
                            details=str(excinfo)),
                    'dialog-error',
                    parent=dialog)
            else:
                if shared.STATUS.document_loaded:
                    database.terminate_session()
                shared.STATUS.document_loaded = False
                move(RUN_DB_FILE, PMDOC_DB_PATH)
                move(RUN_SETUP_FILE, PMDOC_SETUP_PATH)
                database.load_session()
                shared.STATUS.document_modified = False
                shared.STATUS.document_name = doc_name
                shared.STATUS.filters = setting.load()['classes']
                shared.STATUS.document_loaded = True
        dialog.destroy()
