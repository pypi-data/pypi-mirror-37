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

from .tools import ExtDict


def load(filename):
    """Load the values from the toml file."""
    with open(filename) as file_path:
            status = toml.load(file_path)
    return status


def save(data, filename):
    """Save the given file, but updated with given data."""
    with open(filename) as file_path:
        current_status = ExtDict(toml.load(file_path))
    current_status.recursive_update(data)
    with open(filename, 'w') as file_path:
        toml.dump(current_status, file_path)
