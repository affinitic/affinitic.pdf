# -*- coding: utf-8 -*-
"""
affinitic.pdf
-------------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from affinitic.pdf.style import ColumnStyle
from affinitic.pdf.style import RowStyle
from affinitic.pdf.style import Style
from affinitic.pdf.style import TableStyle


class Table(object):

    def __init__(self, pdf, id, style):
        self._columns = []
        self._rows = []
        self._pdf = pdf
        self._id = id
        self.style = style
        if isinstance(self._pdf.get_style(self.style), TableStyle) is False:
            raise ValueError(u'The given table style must be an instance of '
                             u'TableStyle class')

    def add_column(self, title=None, format=None, style=None):
        """Add a new column to the table"""
        if style and isinstance(self._pdf.get_style(style), ColumnStyle) is False:
            raise ValueError(u'The given column style must be an instance of '
                             u'ColumnStyle class')
        self._columns.append(Column(
            'column-%s' % len(self._columns),
            title=title,
            format=format,
            style=style,
        ))

    def add_row(self, content, title=None, style=None):
        """Add a new row to the table"""
        if style and isinstance(self._pdf.get_style(style), RowStyle) is False:
            raise ValueError(u'The given column style must be an instance of '
                             u'RowStyle class')
        content_dict = {}
        if len(content) != len(self._columns):
            raise ValueError("The number of content (%s) doesn't match to the "
                             "number of columns (%s)" % (len(content),
                                                         len(self._columns)))
        for i in range(len(content)):
            content_dict[self._columns[i].name] = content[i]
        self._rows.append(Row(content_dict, title=title, style=style))

    def render(self):
        """Render the table"""
        self.simulate()
        for c_idx, column in enumerate(self._columns):
            for r_idx, row in enumerate(self._rows):
                style = self._get_cell_style(c_idx, column, r_idx, row)
                row_style = self._get_row_style(r_idx, row)

                self._generate_background(style)
                self._pdf.add_paragraph(
                    getattr(row, column.name),
                    width=style.width,
                    height=row_style.height,
                    style=style,
                )
            self._pdf.cursor.move(x=style.width, y=self._height * - 1)
        self._pdf.cursor.move_to(x=0)
        self._pdf.cursor.move(y=self._height)

    def _get_cell_style(self, c_idx, column, r_idx, row):
        c_name = 'table-%s-col-%s' % (self._id, c_idx)
        r_name = 'table-%s-row-%s' % (self._id, r_idx)
        chain = []
        if self._pdf._styles.has_style(c_name):
            chain.append(c_name)
        chain.append(column.style)
        if self._pdf._styles.has_style(r_name):
            chain.append(r_name)
        chain.append(row.style)
        chain.append(self.style)
        return self._get_chain_style(chain)

    def _get_row_style(self, r_idx, row):
        r_name = 'table-%s-row-%s' % (self._id, r_idx)
        chain = []
        if self._pdf._styles.has_style(r_name):
            chain.append(r_name)
        chain.append(row.style)
        return self._get_chain_style(chain)

    def _get_chain_style(self, chain):
        return self._pdf.get_style(
            chain[0],
            inherits=chain[1:],
        )

    def simulate(self):
        """Simulate the table render to handle overflow"""
        for c_idx, column in enumerate(self._columns):
            for r_idx, row in enumerate(self._rows):
                style = self._pdf.get_style(
                    column.style,
                    inherits=[row.style, self.style],
                )
                row_style = self._pdf.get_style(row.style)
                width, height = self._pdf.simulate_paragraph_size(
                    getattr(row, column.name),
                    width=style.width,
                    height=row_style.height,
                    style=style,
                )
                if width > style.width:
                    col_style = Style(width=width)
                    style_id = 'table-%s-col-%s' % (self._id, c_idx)
                    self._pdf._styles.define(style_id, col_style)
                if height > row_style.height:
                    row_style = Style(height=height)
                    style_id = 'table-%s-row-%s' % (self._id, r_idx)
                    self._pdf._styles.define(style_id, row_style)

    def _generate_background(self, style):
        if not style.border and not style.bg_color:
            return
        fill = style.background_color and 1 or 0
        bg_color = style.background_color and style.background_color or None
        stroke_color = style.border_color and style.border_color or None
        stroke = style.border and style.border or 0
        self._pdf.add_rectangle(
            style.width,
            style.height,
            bg_color=bg_color,
            stroke_color=stroke_color,
            fill=fill,
            stroke=stroke,
        )

    @property
    def _height(self):
        """Returns the table height"""
        height = 0
        for r_idx, row in enumerate(self._rows):
            height += self._get_row_style(r_idx, row).height
        return height


class Column(object):

    def __init__(self, name, title=None, format=None, style=None):
        self.name = name
        self.title = title
        self.format = format
        self.style = style


class Row(object):

    def __init__(self, content, title=None, style=None):
        self.title = title
        self.style = style
        for key in content:
            setattr(self, key, content[key])
