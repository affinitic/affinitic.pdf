# -*- coding: utf-8 -*-
"""
Created by mpeeters.
Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by NetExpe sprl
"""

from cStringIO import StringIO

from pyPdf import PdfFileWriter, PdfFileReader
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4

from netexpe.pdf.flowable import ExtendedFlowable
from netexpe.pdf.style import BasicStyles
from netexpe.pdf.table import Table


class Pdf:

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
            leftMargin=margins[3] * measure_unit - 2 * mm)
        self._story = []
        self._currentElement = None
        self._styles = styles or BasicStyles().styles

    def add_element(self):
        """
        Adds a new element in the current story.
        """
        element = ExtendedFlowable(self._measure_unit)
        self._currentElement = element
        self._story.append(element)

    def add_grid(self, size, color):
        """
        Display a grid with the given size and color
        """
        element = ExtendedFlowable(self._measure_unit)
        width = self._document.width / mm
        height = self._document.height / mm
        element.draw_grid(size, width, height, color)
        self._story.insert(0, element)

    def add_style(self, style, style_name):
        """
        Adds a new style that can be used for paragraphs
        """
        self._styles[style_name] = style

    def add_paragraph(self, text, style='paragraph', width=None, height=None):
        """
        Adds a new paragraph element.
        """
        self._verify_element()
        self._currentElement.draw_parapraph(text, self._styles[style],
            width=width, height=height)

    def add_table(self):
        """
        Adds a new table an returns the object
        """
        self._verify_element()
        return Table(self)

    def define_background(self, filepath):
        """
        Defines a pdf file to be set as the background for each pages.
        """
        self._background = filepath

    def write(self, filepath):
        """
        Writes the content of the pdf into the given file.
        """
        self._document.build(self._story)
        f = open(filepath, 'w')
        if hasattr(self, '_background'):
            self._merge_pdf(self._io.getvalue(), f)
        else:
            f.write(self._io.getvalue())
        f.close()

    @property
    def cursor(self):
        """
        Returns the cursor of the current element (flowable).
        """
        self._verify_element()
        return self._currentElement.cursor

    def _verify_element(self):
        """
        Verifies that the current element (flowable) is defined.
        """
        if self._currentElement is None:
            self.add_element()

    def _merge_pdf(self, io_content, output_file):
        """
        Appends the background into the pdf.
        """
        output = PdfFileWriter()
        background = PdfFileReader(open(self._background, 'rb'))
        content_file = file('qsdqsd', 'wb+')
        content_file.write(io_content)
        content = PdfFileReader(content_file)
        for page in content.pages:
            merged_content = background.getPage(0)
            merged_content.mergePage(page)
            output.addPage(merged_content)
        output.write(output_file)
