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

    @property
    def unit(self):
        return self._pdf._measure_unit

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
            style = None
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
            if style is not None:
                self._pdf.cursor.move(
                    x=style.width,
                    y=self._height * - 1,
                )
        self._pdf.cursor.move_to(x=0)
        self._pdf.cursor.move(y=self._height)

    def _get_cell_style(self, c_idx, column, r_idx, row):
        """Return the compound style object for the current cell"""
        cell_name = 'table-%s-cell-%s-%s' % (self._id, r_idx, c_idx)
        col_name = 'table-%s-col-%s' % (self._id, c_idx)
        row_name = 'table-%s-row-%s' % (self._id, r_idx)
        chain = []
        if self._pdf._styles.has_style(cell_name):
            chain.append(cell_name)
        if self._pdf._styles.has_style(col_name):
            chain.append(col_name)
        chain.append(column.style)
        if self._pdf._styles.has_style(row_name):
            chain.append(row_name)
        chain.append(row.style)
        chain.append(self.style)
        return self._get_chain_style(chain)

    def _get_row_style(self, r_idx, row):
        """Return the compound style object for the current row"""
        r_name = 'table-%s-row-%s' % (self._id, r_idx)
        chain = []
        if self._pdf._styles.has_style(r_name):
            chain.append(r_name)
        chain.append(row.style)
        return self._get_chain_style(chain)

    def _get_chain_style(self, chain):
        """Return the compound style object from a chain of styles"""
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
                width, height = self._get_paragraph_infos(row, column, style)
                self._adapt_size(width, height, style, c_idx, r_idx)
        for c_idx, column in enumerate(self._columns):
            for r_idx, row in enumerate(self._rows):
                style = self._get_cell_style(c_idx, column, r_idx, row)
                width, height = self._get_paragraph_infos(row, column, style)
                self._adapt_position(width, height, style, c_idx, r_idx)

    def _get_paragraph_infos(self, row, column, style):
        """Return the simulate width and height of the paragraph"""
        width, height = self._pdf.simulate_paragraph_size(
            getattr(row, column.name),
            width=style.width,
            height=style.height,
            style=style,
        )
        return width, height

    def _adapt_size(self, width, height, style, c_idx, r_idx):
        """Create specific styles for row or column"""
        c_name = 'table-%s-col-%s' % (self._id, c_idx)
        r_name = 'table-%s-row-%s' % (self._id, r_idx)
        if width > style.width:
            self._create_style(c_name, width=(width + style.padding_h))
        if height > style.height:
            self._create_style(r_name, height=height)

    def _adapt_position(self, width, height, style, c_idx, r_idx):
        """Create specific styles for cells"""
        cell_name = 'table-%s-cell-%s-%s' % (self._id, r_idx, c_idx)
        if height < style.height and style.vertical_align is 'middle':
            space_before = style.space_before + (style.height - height) / 2
            self._create_style(cell_name, space_before=space_before)
        if height < style.height and style.vertical_align is 'bottom':
            space_before = style.space_before + (style.height - height)
            self._create_style(cell_name, space_before=space_before)

    def _create_style(self, stylename, **kwargs):
        if self._pdf._styles.has_style(stylename):
            style = self._pdf._styles.get_specific(stylename)
        else:
            style = Style(**kwargs)
        for key, value in kwargs.items():
            if hasattr(style, key) and getattr(style, key) > value:
                continue
            setattr(style, key, value)
        self._pdf._styles.define(stylename, style)

    def _generate_background(self, style):
        """Generate the background for a table cell"""
        if not style.border and not style.background_color:
            return
        fill = style.background_color and 1 or 0
        bg_color = style.background_color and style.background_color or None
        stroke_color = style.border_color and style.border_color or None
        stroke = style.border and style.border or 0
        self._pdf.add_rectangle(
            style.width,
            style.height + style.padding_v,
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
            style = self._get_row_style(r_idx, row)
            height += style.height + style.padding_v
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
