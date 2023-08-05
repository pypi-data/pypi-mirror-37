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
from tarfile import is_tarfile
from gettext import translation
from itertools import zip_longest
from decimal import InvalidOperation

import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('Pango', '1.0')
except ValueError:
    raise
else:
    from gi.repository import Gtk, Pango

from mathmakerlib.calculus import Number

from . import shared, constants
from .env import L10N_DOMAIN, LOCALEDIR

STEPS = constants.NUMERIC_STEPS


def turn_to_capwords(name):
    return ''.join(x.capitalize() for x in name.split('_'))


def grouper(iterable, n, padvalue=None):
    """
    grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')
    """
    # Taken from https://stackoverflow.com/a/312644/3926735
    return zip_longest(*[iter(iterable)] * n, fillvalue=padvalue)


def is_cot_file(path):
    return os.path.isfile(path) and is_tarfile(path)


def cot_filter(filter_info, data):
    path = filter_info.filename
    return is_cot_file(path) and path.endswith('.tgz')


def add_filter_any(dialog):
    tr = translation(L10N_DOMAIN, LOCALEDIR, [shared.PREFS.language]).gettext
    filter_any = Gtk.FileFilter()
    filter_any.set_name(tr('Any files'))
    filter_any.add_pattern('*')
    dialog.add_filter(filter_any)


def add_cot_filters(dialog):
    tr = translation(L10N_DOMAIN, LOCALEDIR, [shared.PREFS.language]).gettext

    filter_cot = Gtk.FileFilter()
    filter_cot.set_name(tr('Cotinga files'))
    filter_cot.add_custom(Gtk.FileFilterFlags.FILENAME, cot_filter, None)
    dialog.add_filter(filter_cot)

    add_filter_any(dialog)


def add_pdf_filters(dialog):
    tr = translation(L10N_DOMAIN, LOCALEDIR, [shared.PREFS.language]).gettext

    filter_pdf = Gtk.FileFilter()
    filter_pdf.set_name(tr('Any pdf file'))
    filter_pdf.add_mime_type('application/pdf')
    dialog.add_filter(filter_pdf)

    add_filter_any(dialog)


def check_grade(cell_text, special_grades, grading):
    result = (True, True)
    if cell_text in special_grades:
        result = (True, False)
    else:
        if grading['choice'] == 'numeric':
            if cell_text in ['', None]:
                result = (False, False)
            else:
                try:
                    nb = Number(cell_text.replace(',', '.'))
                except InvalidOperation:
                    result = (False, False)
                else:
                    if (nb < Number(grading['minimum'])
                            or nb > Number(grading['maximum'])
                            or nb % Number(STEPS[grading['step']])):
                        result = (False, False)
        else:  # grading['choice'] is 'literal'
            if cell_text not in grading['literal_grades']:
                result = (False, False)
    return result


def cellfont_fmt(cell_text, special_grades, grading):
    # LATER: use theme foreground color instead of black
    paint_it = 'Black'
    weight = int(Pango.Weight.NORMAL)
    accepted, regular = check_grade(cell_text, special_grades, grading)
    if accepted:
        if not regular:
            paint_it = 'Grey'
    else:
        paint_it = 'Firebrick'
        weight = int(Pango.Weight.BOLD)
    return (paint_it, weight)


def grade_ge_edge(grading, grade, special_grades):
    accepted, regular = check_grade(grade, special_grades, grading)
    if accepted and regular:
        if grading['choice'] == 'numeric':
            edge = grading['edge_numeric']
            return Number(grade.replace(',', '.')) >= Number(edge)
        else:  # grading['choice'] == 'literal'
            edge = grading['edge_literal']
            return grading['literal_grades'].index(grade) \
                >= grading['literal_grades'].index(edge)
    else:
        return False


def calculate_attained_level(start_level, levels, grading, grades,
                             special_grades):
    # LATER: check start_level belongs to levels?
    index = levels.index(start_level)
    for grade in grades:
        if grade_ge_edge(grading, grade, special_grades):
            index += 1
    try:
        result = levels[index]
    except IndexError:
        result = levels[-1]
    return result


def build_view(*cols, xalign=None, set_cell_func=None):
    """
    Example: build_view(['Title1', 'data1', 'data2'],
                        ['Title2', 'data3', 'data4'])

    :param cols: the columns contents, starting with title
    :type cols: list
    :rtype: Gtk.TreeView
    """
    store = Gtk.ListStore(*([str] * len(cols)))
    for i, row in enumerate(zip(*cols)):
        if i:  # we do not add the first data, being the title
            store.append(row)
    view = Gtk.TreeView(store)
    view.props.margin = 10
    view.get_selection().set_mode(Gtk.SelectionMode.NONE)
    for i, col in enumerate(cols):
        rend = Gtk.CellRendererText()
        if xalign is not None:
            rend.props.xalign = xalign[i]
        view_col = Gtk.TreeViewColumn(col[0], rend, text=i)
        if set_cell_func is not None and set_cell_func[i] is not None:
            view_col.set_cell_data_func(rend, set_cell_func[i])
        view.append_column(view_col)
    return view


class ExtDict(dict):
    """A dict with more methods."""

    def recursive_update(self, d2):
        """
        Update self with d2 key/values, recursively update nested dicts.

        :Example:

        >>> d = ExtDict({'a': 1, 'b': {'a': 7, 'c': 10}})
        >>> d.recursive_update({'a': 24, 'd': 13, 'b': {'c': 100}})
        >>> print(d == {'a': 24, 'd': 13, 'b': {'a': 7, 'c': 100}})
        True
        >>> d = ExtDict()
        >>> d.recursive_update({'d': {'f': 13}})
        >>> d
        {'d': {'f': 13}}
        >>> d = ExtDict({'a': 1, 'b': {'a': 7, 'c': 10}})
        >>> d.recursive_update({'h': {'z': 49}})
        >>> print(d == {'a': 1, 'b': {'a': 7, 'c': 10}, 'h': {'z': 49}})
        True
        """
        nested1 = {key: ExtDict(val)
                   for key, val in iter(self.items())
                   if isinstance(val, dict)}
        other1 = {key: val
                  for key, val in iter(self.items())
                  if not isinstance(val, dict)}
        nested2 = {key: val
                   for key, val in iter(d2.items())
                   if isinstance(val, dict)}
        other2 = {key: val
                  for key, val in iter(d2.items())
                  if not isinstance(val, dict)}
        other1.update(other2)
        for key in nested1:
            if key in nested2:
                nested1[key].recursive_update(nested2[key])
        for key in nested2:
            if key not in nested1:
                nested1[key] = nested2[key]
        other1.update(nested1)
        self.update(other1)


class Listing(object):

    def __init__(self, data, data_row=None, position=None):
        """
        data may be None or a list or any other type
        prepend must be None or a list
        """
        if data_row is None:
            data_row = []
        if not isinstance(data_row, list):
            raise TypeError('Argument data_row should be a list, found {} '
                            'instead'.format(str(type(data_row))))
        if data is None:
            data = []
        if not isinstance(data, list):
            data = [data]
        self.cols = [item for item in data_row]
        if position is None:
            position = len(self.cols)
        for i, item in enumerate(data):
            retry = True
            while retry:
                try:
                    self.cols[position + i] = item
                except IndexError:
                    self.cols.append('')
                else:
                    retry = False

    def __iter__(self):
        return iter(self.cols)

    def __str__(self):
        return str(self.cols)

    def __repr__(self):
        return 'Listing({})'.format(self.cols)
