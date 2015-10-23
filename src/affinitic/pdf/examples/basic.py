# -*- coding: utf-8 -*-
"""
affinitic.pdf
-------------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

import os

from affinitic.pdf.pdf import Pdf
from affinitic.pdf.style import Style
from affinitic.pdf.style import StyleLibrary
from affinitic.pdf.tools import ColorRGB


class BasicPdf(object):

    def __init__(self):
        self.pdf = Pdf(margins=[29, 15, 15, 15], styles=self.styles)
        self.pdf.define_background(os.path.join(self.current_path,
                                                'background.pdf'))

    @property
    def current_path(self):
        return os.path.split(os.path.abspath(__file__))[0]

    @property
    def styles(self):
        base_style = Style(color=ColorRGB(50, 50, 50), text_align='justify')
        library = StyleLibrary(base_style=base_style)
        library.add('title', Style(text_indent=2, font_size=18))
        library.add('first', Style(first_line_indent=10))
        library.add('red', Style(color=ColorRGB(255, 0, 0), padding='3'))
        return library

    def create_pdf(self):
        # Title
        self.pdf.add_h_line()
        self.pdf.cursor.move(y=5)
        self.pdf.add_paragraph('Title', style='title')
        self.pdf.cursor.move(y=5)
        self.pdf.add_h_line()

        # Content
        self.pdf.cursor.move(y=10)
        self.pdf.add_paragraph('''
Donec eu eros sit amet metus finibus dignissim. Aenean purus arcu, facilisis non placerat in, commodo non mi. Mauris vel placerat purus. Morbi at placerat tortor. Aenean pretium lectus et magna dictum, id venenatis mauris laoreet. Sed euismod vel justo sed ultricies. Donec sed urna nec eros venenatis posuere. Vivamus facilisis blandit orci ac consectetur.
        ''', style='first')
        self.pdf.cursor.move(y=5)
        self.pdf.add_paragraph('''
Fusce ornare erat sit amet augue volutpat, nec porttitor metus venenatis. Fusce nec urna augue. Integer finibus vestibulum convallis. Mauris eget dapibus ipsum, mattis luctus mi. Donec faucibus, lacus in vestibulum venenatis, lacus massa fermentum neque, et convallis arcu lacus eget metus. In blandit nunc ut sem porta ullamcorper. Mauris a mi commodo, sollicitudin arcu sed, maximus mauris. Quisque vel facilisis felis, eu auctor enim.
        ''', style='red')
        self.pdf.cursor.move(y=5)
        self.pdf.add_paragraph('''
Maecenas ut tincidunt nunc. Sed ipsum justo, porta sed elit rutrum, suscipit fermentum urna. Pellentesque sagittis elit nec elit tristique tempor et eu risus. Curabitur nec nibh at justo vehicula cursus eget facilisis eros. In tempus est quis nunc venenatis sodales. Duis id lacus sed eros convallis imperdiet. Pellentesque eget ex eros.
        ''')

        self.pdf.write('basic.pdf')


def main():
    pdf = BasicPdf()
    pdf.create_pdf()
    print 'The file basic.pdf was generated'
