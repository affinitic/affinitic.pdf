# -*- coding: utf-8 -*-
"""
affinitic.pdf
-------------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from affinitic.pdf.style import TableStyle


class Table(object):

    def __init__(self, pdf, style):
        self._columns = []
        self._rows = []
        self._pdf = pdf
        self.style = style
        if isinstance(self._pdf.get_style(self.style), TableStyle) is False:
            raise ValueError(u'The given style must be an instance of '
                             u'TableStyle class')

    def add_column(self, title=None, format=None, style=None):
        """Add a new column to the table"""
        self._columns.append(Column(
            'column-%s' % len(self._columns),
            title=title,
            format=format,
            style=style,
        ))

    def add_row(self, content, title=None, style=None):
        """Add a new row to the table"""
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
        for column in self._columns:
            for row in self._rows:
                style = self._pdf.get_style(
                    column.style,
                    inherits=[row.style, self.style],
                )
                row_style = self._pdf.get_style(row.style)

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
        for row in self._rows:
            height += self._pdf._styles.get(row.style).height
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
