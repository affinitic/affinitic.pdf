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
from reportlab.lib.pagesizes import landscape
from reportlab.lib.pagesizes import portrait
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.flowables import PageBreak

from affinitic.pdf.element import DeferredElement
from affinitic.pdf.flowable import ExtendedFlowable
from affinitic.pdf.flowable import SimulationFlowable
from affinitic.pdf.style import Style
from affinitic.pdf.style import StyleLibrary
from affinitic.pdf.table import Table
from affinitic.pdf.tools import ColorRGB


class Pdf(object):
    _simulation_doc = None
    _orientations = {
        'portrait': portrait,
        'landscape': landscape,
    }

    def __init__(self,
                 format=A4,
                 orientation='portrait',
                 margins=[10, 10, 10, 10],
                 measure_unit=mm,
                 styles=None,
                 header=None,
                 footer=None,
                 debug=False,
                 localizer=None):
        self._io = StringIO()
        self._format = format
        self._orientation = self._orientations.get(orientation)
        self._margins = margins
        self._measure_unit = measure_unit
        self._document = self._create_document(self._io)
        self._story = []
        self._currentElement = None
        self._styles = styles or StyleLibrary()
        self._debug = debug
        self._header = header
        self._footer = footer
        self._page_counter = 1
        self._current_height = 0.0
        self._uids = []

        self.localizer = localizer

        if self._debug is True:
            self.add_grid(5, ColorRGB(200, 0, 0, alpha=50))
        if self._header:
            self._story.append(self._header(self))

    def _create_document(self, io):
        return SimpleDocTemplate(
            io,
            pagesize=self._orientation(self._format),
            topMargin=self._margins[0] * self._measure_unit - 2 * mm,
            rightMargin=self._margins[1] * self._measure_unit + 2 * mm,
            bottomMargin=self._margins[2] * self._measure_unit + 2 * mm,
            leftMargin=self._margins[3] * self._measure_unit - 2 * mm,
        )

    def _get_simulation_document(self):
        if not self._simulation_doc:
            self._simulation_doc = self._create_document(StringIO())
            self._simulation_doc.build([])
        return self._simulation_doc

    @property
    def page_number(self):
        return self._page_counter

    @property
    def width(self):
        """Return the document width"""
        doc = self._document
        width = doc.width / self._measure_unit
        return width

    @property
    def height(self):
        """Return the document height"""
        doc = self._document
        height = doc.height / self._measure_unit
        return height

    @property
    def current_height(self):
        """Return the current element height"""
        return self._current_height

    def _adapt_height(self, height):
        width, height = self.cursor._apply_changes(0, height)
        self._current_height += height
        self.cursor._track_changes()

    def add_page_break(self):
        """Add a page break element"""
        if self._footer:
            self._story.append(self._footer(self))
        self._story.append(PageBreak())
        if self._header:
            self._story.append(self._header(self))
        self._page_counter += 1
        if self._debug is True:
            self.add_grid(5, ColorRGB(200, 0, 0, alpha=50))
        self._current_height = 0.0
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
        self._story.append(element)

    def add_style(self, stylename, style, inherits=None):
        """Add a new style"""
        self._styles.define(stylename, style, inherits=None)

    def get_style(self, style, inherits=None):
        """Return the style for the given style name"""
        if isinstance(style, Style):
            return style
        return self._styles.get(style, inherits=inherits)

    def add_paragraph(self, text, style='paragraph', width=None, height=None):
        """Add a new paragraph element"""
        self._verify_element()
        style = self.get_style(style)
        self._currentElement.draw_paragraph(
            text,
            style,
            width=width,
            height=height,
            debug=self._debug,
        )
        width, height = self.simulate_paragraph_size(
            text,
            style.name,
            width,
            height,
        )
        if height < style.height:
            height = style.height
        self._adapt_height(height + style.padding_v)

    def simulate_paragraph_size(
            self,
            text,
            style='paragraph',
            width=None,
            height=None):
        """Return the simulated paragraph size"""
        document = self._get_simulation_document()
        element = SimulationFlowable(self._measure_unit, document)
        return element.paragraph_size(
            text,
            self.get_style(style),
            width=width,
            height=height,
        )

    def add_table(self, id, style=None):
        """Add a new table an returns the object"""
        self._verify_element()
        if id in self._uids:
            raise ValueError("The table id must be unique")
        self._uids.append(id)
        return Table(self, id, self.get_style(style).name)

    def add_h_line(self, color=ColorRGB(50, 50, 50)):
        """Add a horizontal line"""
        self._verify_element()
        self._currentElement.draw_h_line(
            self._document.width / mm,
            color=color,
        )

    def add_rectangle(
            self,
            width,
            height,
            bg_color=ColorRGB(240, 240, 240),
            stroke_color=ColorRGB(150, 150, 150),
            fill=1,
            stroke=0):
        """Add a rectangle"""
        self._verify_element()
        self._currentElement.draw_rectangle(
            width,
            height,
            bg_color=bg_color,
            stroke_color=stroke_color,
            fill=fill,
            stroke=stroke,
        )

    def add_barcode(self, value, barHeight=None, barWidth=0.75):
        """Add a barcode"""
        self._verify_element()
        self._currentElement.draw_barcode(value, barHeight, barWidth)

    def add_image(self, img_path, width=None, height=None):
        """Add an image"""
        self._verify_element()
        self._currentElement.draw_image(img_path, width=width, height=height)

    def define_background(self, filepath):
        """Define a pdf file to be set as the background for each pages"""
        self._background = filepath

    @property
    def content(self):
        """Return the content of the pdf"""
        if self._footer:
            self._story.append(self._footer(self))
        self._render_deferred_elements()
        self._document.build(self._story)
        if hasattr(self, '_background'):
            content = StringIO()
            self._merge_pdf(self._io.getvalue(), content)
            return content.getvalue()
        else:
            return self._io.getvalue()

    def _render_deferred_elements(self):
        """Render the deferred elements like footers or headers"""
        for element in self._story:
            if isinstance(element, DeferredElement):
                element._render()

    def write(self, filepath):
        """Write the content of the pdf into the given file"""
        f = open(filepath, 'w')
        f.write(self.content)
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
        bg_file = open(self._background, 'r')
        with open("/tmp/merge.pdf", "w") as f:
            f.write(io_content)
        with open("/tmp/merge.pdf", "r") as f:
            content = PdfFileReader(f)
            for page in content.pages:
                bg_file.seek(0)
                new_content = PdfFileReader(bg_file).getPage(0)
                new_content.mergePage(page)
                output.addPage(new_content)
            output.write(output_file)
