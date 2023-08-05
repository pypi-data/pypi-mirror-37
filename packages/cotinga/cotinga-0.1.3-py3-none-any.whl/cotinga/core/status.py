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
from shutil import copyfile

from . import io
from .env import STATUS_FILE, DEFAULT_STATUS_FILE


def load():
    """Load the values from the toml status file."""
    if not os.path.isfile(STATUS_FILE):  # Should only happen at first run
        copyfile(DEFAULT_STATUS_FILE, STATUS_FILE)
    return io.load(STATUS_FILE)


def save(data):
    """Save the status file updated with given data."""
    io.save(data, STATUS_FILE)
