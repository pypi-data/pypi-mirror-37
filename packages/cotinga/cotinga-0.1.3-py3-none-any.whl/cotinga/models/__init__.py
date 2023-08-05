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

import sys

from .pupils import Pupils, pupils_columns, pupils_tablename, PUPILS_COL_NBS

this = sys.modules[__name__]

__all__ = ['Pupils', 'pupils_columns', 'pupils_tablename', 'PUPILS_COL_NBS']

TABLENAMES = [item[:-len('_tablename')]
              for item in __all__
              if item.endswith('_tablename')]

COLNAMES = {tablename: [col.name
                        for col in getattr(this,
                                           '{}_columns'.format(tablename))()]
            for tablename in TABLENAMES}
