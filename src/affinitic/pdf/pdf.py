# -*- coding: utf-8 -*-
"""
affinitic.pdf
-------------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from cStringIO import StringIO
from pyPdf import PdfFileWriter, PdfFileReader
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.flowables import PageBreak

from affinitic.pdf.flowable import ExtendedFlowable
from affinitic.pdf.style import StyleLibrary
from affinitic.pdf.table import Table
from affinitic.pdf.tools import ColorRGB


class Pdf(object):

    def __init__(self,
                 format=A4,
                 margins=[10, 10, 10, 10],
                 measure_unit=mm,
                 styles=None):
        self._measure_unit = measure_unit
        self._io = StringIO()
        self._document = SimpleDocTemplate(
            self._io,
            pagesize=format,
            topMargin=margins[0] * measure_unit - 2 * mm,
            rightMargin=margins[1] * measure_unit + 2 * mm,
            bottomMargin=margins[2] * measure_unit + 2 * mm,
            leftMargin=margins[3] * measure_unit - 2 * mm,
        )
        self._story = []
        self._currentElement = None
        self._styles = styles or StyleLibrary()

    @property
    def width(self):
        """Return the document width"""
        doc = self._document
        width = doc.width / self._measure_unit
        margin = (doc.rightMargin + doc.leftMargin) / self._measure_unit
        return width - margin

    @property
    def height(self):
        """Return the document height"""
        doc = self._document
        height = doc.height / self._measure_unit
        margin = (doc.topMargin + doc.bottomMargin) / self._measure_unit
        return height - margin

    def add_page_break(self):
        """Add a page break element"""
        self._story.append(PageBreak())
        self.add_element()

    def add_element(self):
        """Add a new element in the current story"""
        element = ExtendedFlowable(self._measure_unit)
        self._currentElement = element
        self._story.append(element)

    def add_grid(self, size, color):
        """Display a grid with the given size and color"""
        element = ExtendedFlowable(self._measure_unit)
        width = self._document.width / mm
        height = self._document.height / mm
        element.draw_grid(size, width, height, color)
        self._story.insert(0, element)

    def add_style(self, stylename, style):
        """Add a new style"""
        self._styles.define(stylename, style)

    def add_paragraph(self, text, style='paragraph', width=None, height=None):
        """Add a new paragraph element"""
        self._verify_element()
        self._currentElement.draw_parapraph(
            text,
            self._styles.get(style),
            width=width,
            height=height,
        )

    def add_table(self):
        """Add a new table an returns the object"""
        self._verify_element()
        return Table(self)

    def add_h_line(self, color=ColorRGB(50, 50, 50)):
        """Add a horizontal line"""
        self._verify_element()
        self._currentElement.draw_h_line(
            self._document.width / mm,
            color=color,
        )

    def add_rectangle(self, width, height, bg_color=ColorRGB(240, 240, 240)):
        """Add a rectangle"""
        self._verify_element()
        self._currentElement.draw_rectangle(
            width,
            height,
            bg_color=bg_color,
            fill=1,
            stroke=0,
        )

    def define_background(self, filepath):
        """Define a pdf file to be set as the background for each pages"""
        self._background = filepath

    def write(self, filepath):
        """Write the content of the pdf into the given file"""
        self._document.build(self._story)
        f = open(filepath, 'w')
        if hasattr(self, '_background'):
            self._merge_pdf(self._io.getvalue(), f)
        else:
            f.write(self._io.getvalue())
        f.close()

    @property
    def cursor(self):
        """Return the cursor of the current element (flowable)"""
        self._verify_element()
        return self._currentElement.cursor

    def _verify_element(self):
        """Verify that the current element (flowable) is defined"""
        if self._currentElement is None:
            self.add_element()

    def _merge_pdf(self, io_content, output_file):
        """Add the background into the pdf"""
        output = PdfFileWriter()
        background = PdfFileReader(open(self._background, 'rb'))
        content_file = file('/tmp/merge.pdf', 'wb+')
        content_file.write(io_content)
        content = PdfFileReader(content_file)
        for page in content.pages:
            background_content = background.getPage(0)
            page.mergePage(background_content)
            output.addPage(page)
        output.write(output_file)
