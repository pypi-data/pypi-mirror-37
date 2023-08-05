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

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy_utils import ScalarListType

from cotinga.core import constants

SEP = constants.INTERNAL_SEPARATOR

pupils_tablename = 'pupils'
PUPILS_COL_NBS = {'id': 0, 'included': 1, 'classname': 2, 'fullname': 3,
                  'initial_level': 4, 'attained_level': 5, 'grades': 6}


class Pupils(object):

    def __init__(self, included, classname, fullname, initial_level,
                 attained_level, grades):
        self.included = included
        self.classname = classname
        self.fullname = fullname
        self.initial_level = initial_level
        self.attained_level = attained_level
        self.grades = grades

    def __repr__(self):
        return 'Pupils(included={}, classname={}, fullname={}, '\
            'initial_level={}, attained_level={}, grades={})'\
            .format(repr(self.included), repr(self.classname),
                    repr(self.fullname), repr(self.initial_level),
                    repr(self.attained_level), repr(self.grades))


def pupils_columns():
    return (Column('id', Integer, primary_key=True),
            Column('included', Boolean),
            Column('classname', String),
            Column('fullname', String),
            Column('initial_level', String),
            Column('attained_level', String),
            Column('grades', ScalarListType(separator=SEP)),
            )
