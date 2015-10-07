# -*- coding: utf-8 -*-
"""
affinitic.pdf
-------------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from affinitic.pdf.pdf import Pdf
from affinitic.pdf.style import ColumnStyle
from affinitic.pdf.style import RowStyle
from affinitic.pdf.style import TableStyle
from affinitic.pdf.style import Style
from affinitic.pdf.style import StyleLibrary
from affinitic.pdf.tools import ColorRGB


class TablePdf(object):

    def __init__(self):
        self.pdf = Pdf(margins=[15, 15, 15, 15], styles=self.styles)

    @property
    def styles(self):
        base_style = Style(color=ColorRGB(50, 50, 50), text_align='left')
        library = StyleLibrary(base_style=base_style)
        library.add('col1', ColumnStyle(width=10))
        library.add('col2', ColumnStyle(width=50))
        library.add('col3', ColumnStyle(width=30))
        library.add(
            'table',
            TableStyle(
                border=1,
                background_color=ColorRGB(230, 230, 230),
                border_color=ColorRGB(90, 90, 90),
                padding='3',
            ),
        )
        library.add(
            'header',
            RowStyle(
                height=10,
                font_size=10,
                background_color=ColorRGB(50, 50, 50),
                color=ColorRGB(255, 255, 255),
                vertical_align='middle',
            ),
            inherits=['table'],
        )
        library.add(
            'footer',
            RowStyle(
                height=10,
                background_color=ColorRGB(150, 150, 150),
                vertical_align='bottom',
            ),
            inherits=['table'],
        )
        library.add('odd', RowStyle(height=0), inherits=['table'])
        library.add(
            'even',
            RowStyle(background_color=ColorRGB(190, 190, 190)),
            inherits=['odd'],
        )
        return library

    def create_pdf(self):
        table = self.pdf.add_table('tableid', style='table')
        table.add_column(style='col1')
        table.add_column(style='col2')
        table.add_column(style='col3')
        table.add_row([u'Title 1', u'Title 2', u'Title 3'], style='header')

        for idx, row in enumerate(self.content):
            style = idx % 2 and 'even' or 'odd'
            table.add_row(row, style=style)
        table.add_row([u'Footer 1', u'Footer 2', u'Footer 3'], style='footer')
        table.render()
        self.pdf.write('table.pdf')

    @property
    def content(self):
        return (
            ['L1.1', 'L1.2', 'L1.3'],
            ['L2.1', 'L2.2', 'L2.3<br/>lorem ipsum dolor sit amet'],
            ['L3.1-1-1-1-1', 'L3.2', 'L3.3'],
            ['L4.1', 'L4.2', 'L4.3'],
        )


def main():
    pdf = TablePdf()
    pdf.create_pdf()
    print 'The file table.pdf was generated'
