# -*- coding: utf-8 -*-
"""
Created by mpeeters.
Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by NetExpe sprl
"""


class Table:

    def __init__(self, pdf):
        self._columns = []
        self._rows = []
        self._pdf = pdf

    def add_column(self, title=None, format=None, style=None):
        """
        Adds a new column to the table
        """
        self._columns.append(Column('column-%s' % len(self._columns),
            title=title, format=format, style=style))

    def add_row(self, content, title=None, style=None):
        """
        Adds a new row to the table
        """
        content_dict = {}
        if len(content) != len(self._columns):
            raise ValueError("The number of content (%s) doesn't match to the "
                "number of columns (%s)" % (len(content), len(self._columns)))
        for i in range(len(content)):
            content_dict[self._columns[i].name] = content[i]
        self._rows.append(Row(content_dict, title=title, style=style))

    def render(self):
        """
        Render the table
        """
        for column in self._columns:
            for row in self._rows:
                self._pdf.add_paragraph(
                    getattr(row, column.name),
                    width=column.style.width,
                    height=row.style.height)
            self._pdf.cursor.move(x=column.style.width, y=self._height * - 1)

    @property
    def _height(self):
        """
        Returns the table height.
        """
        height = 0
        for row in self._rows:
            height += row.style.height
        return height


class Column:

    def __init__(self, name, title=None, format=None, style=None):
        self.name = name
        self.title = title
        self.format = format
        self.style = style


class Row:

    def __init__(self, content, title=None, style=None):
        self.title = title
        self.style = style
        for key in content:
            setattr(self, key, content[key])
