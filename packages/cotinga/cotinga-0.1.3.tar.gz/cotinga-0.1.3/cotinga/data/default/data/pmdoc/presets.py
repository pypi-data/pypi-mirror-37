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

from cotinga.core.shared import PREFS
from cotinga.core.env import LOCALEDIR, L10N_DOMAIN


def GRADES_SCALES():
    tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
    return \
        {'ABCDE': ('A, B, C, D, E', ['A', 'B', 'C', 'D', 'E']),
         'ABCDF': (tr('A, B, C, D, F (US style)'), ['A', 'B', 'C', 'D', 'F']),
         'ABCDE_signed': (tr('A, B, C, D, E with signs'),
                          ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-',
                           'D+', 'D', 'D-', 'E+', 'E']),
         'ABCDF_signed': (tr('A, B, C, D, F with signs (US style)'),
                          ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-',
                           'D+', 'D', 'D-', 'F'])
         }


def LEVELS_SCALES():
    tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
    return \
        {'karate': (tr('Karate-like (7 belts: white, yellow, ...)'),
                    [tr('White belt'), tr('Yellow belt'), tr('Orange belt'),
                     tr('Green belt'), tr('Blue belt'), tr('Brown belt'),
                     tr('Black belt')]),
         'judo': (tr('Judo-like (12 belts: white, white & yellow, ...)'),
                  [tr('White belt'), tr('White and yellow belt'),
                   tr('Yellow belt'), tr('Yellow and orange belt'),
                   tr('Orange belt'), tr('Orange and green belt'),
                   tr('Green belt'), tr('Blue belt'), tr('Brown belt'),
                   tr('Black belt'), tr('Red and white belt'),
                   tr('Red belt')]),
         'martial-arts-extended': (tr('Martial arts-like (22 belts: white, '
                                      'white 1st stripe, ...)'),
                                   [tr('White belt'),
                                    tr('White belt |'),
                                    tr('White belt ||'),
                                    tr('Yellow belt'),
                                    tr('Yellow belt |'),
                                    tr('Yellow belt ||'),
                                    tr('Orange belt'),
                                    tr('Orange belt |'),
                                    tr('Orange belt ||'),
                                    tr('Green belt'),
                                    tr('Green belt |'),
                                    tr('Green belt ||'),
                                    tr('Blue belt'),
                                    tr('Blue belt |'),
                                    tr('Blue belt ||'),
                                    tr('Brown belt'),
                                    tr('Brown belt |'),
                                    tr('Brown belt ||'),
                                    tr('Red belt'),
                                    tr('Red belt |'),
                                    tr('Red belt ||'),
                                    tr('Black belt'),
                                    ])
         }
