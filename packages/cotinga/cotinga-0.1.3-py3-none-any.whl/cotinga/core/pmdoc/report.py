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

from datetime import datetime
from gettext import translation

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from ..env import REPORT_FILE, LOCALEDIR, L10N_DOMAIN
from ..tools import grouper
from .. import shared

DARK_GRAY = colors.HexColor(0x333333)
DIM_GRAY = colors.HexColor(0x808080)

MAX_NB_PER_COL = 30


def rework_data(data):
    PREFS = shared.PREFS
    tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
    col_data = []
    spans = []
    classes = set()
    for col in data:
        title = tr('{level} ({nb})').format(level=col[0], nb=col[1])
        names = sorted([pupil.fullname for pupil in col[2]])
        classes |= set([pupil.classname for pupil in col[2]])
        for i, lst in enumerate(grouper(names, MAX_NB_PER_COL, padvalue='')):
            if i:
                new_col = ['']
                spans.append(True)
            else:
                new_col = [title]  # copy title in the first column
                spans.append(False)
            new_col += lst
            col_data.append(new_col)
    maxi = max([len(item) for item in col_data] + [0])
    report_data = []
    for i in range(maxi):
        new_row = [item[i:i + 1] or ['']
                   for item in col_data]
        report_data.append([p[0] for p in new_row])
    spans.append(False)
    return report_data, spans, classes


def workout_spans(spans):
    result = []
    start_span = None
    for i, span in enumerate(spans):
        if start_span is None:
            if span:
                start_span = i - 1
        else:
            if not span:
                result.append(('SPAN', (start_span, 0), (i - 1, 0)))
                start_span = None
    return result


def build(data):
    data, spans, classes = rework_data(data)
    PREFS = shared.PREFS
    tr = translation(L10N_DOMAIN, LOCALEDIR, [PREFS.language]).gettext
    stylesheet = getSampleStyleSheet()
    title_style = stylesheet['Title']
    title_style.spaceAfter = 0.5 * cm
    h2_style = stylesheet['Heading3']
    h2_style.spaceAfter = 0.5 * cm
    doc = SimpleDocTemplate(REPORT_FILE, pagesize=landscape(A4),
                            leftMargin=0 * cm, rightMargin=0 * cm,
                            topMargin=0 * cm, bottomMargin=0 * cm)

    elements = []
    last_sep = ' {} '.format(tr('and'))
    classes_list = last_sep.join(sorted(list(classes)))
    classes_list = classes_list.replace(last_sep, ', ', len(classes) - 2)
    header = Paragraph(tr('Next evaluation ({classes_list})')
                       .format(classes_list=classes_list),
                       title_style)
    elements.append(header)

    date_fmt = PREFS.pmreport['date_fmt']
    date = datetime.now().strftime(date_fmt)

    subheader = Paragraph(tr('Following levels will be attempted '
                             '(update {date})').format(date=date),
                          h2_style)
    elements.append(subheader)

    ncol = len(data[0])
    nrow = len(data)

    # LATER: adapt col width and height
    t = Table(data, ncol * [5.5 * cm], nrow * [0.5 * cm])

    col_separators = [('LINEAFTER', (i, 0), (i, nrow), 1, DIM_GRAY)
                      for i in range(ncol - 1)
                      if not spans[(i + 1)]]

    t.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           ('TEXTCOLOR', (0, 0), (-1, -1), DARK_GRAY),
                           ('LINEABOVE', (0, 1), (ncol, 1), 1, DIM_GRAY)
                           ] + col_separators + workout_spans(spans)))

    elements.append(t)
    # write the document to disk
    doc.build(elements)
