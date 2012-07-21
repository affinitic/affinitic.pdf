# -*- coding: utf-8 -*-
"""
Created by mpeeters.
Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by NetExpe sprl
"""

from cStringIO import StringIO

from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4

from netexpe.pdf.flowable import ExtendedFlowable
from netexpe.pdf.style import BasicStyles


class Pdf(object):

    def __init__(self,
            format=A4,
            margins=[10, 10, 10, 10],
            measure_unit=mm,
            styles=BasicStyles().styles):
        self._measure_unit = measure_unit
        self._file = StringIO()
        self._document = SimpleDocTemplate(
            self._file,
            pagesize=format,
            topMargin=margins[0] * measure_unit,
            rightMargin=margins[1] * measure_unit,
            bottomMargin=margins[2] * measure_unit,
            leftMargin=margins[3] * measure_unit)
        self._story = []
        self._currentElement = None
        self._styles = styles

    def add_element(self):
        """
        Adds a new element in the current story.
        """
        element = ExtendedFlowable(self._measure_unit)
        self._currentElement = element
        self._story.append(element)

    def add_style(self, style, style_name):
        """
        Adds a new style that can be used for paragraphs
        """
        self._styles[style_name] = style

    def add_paragraph(self, text, style='paragraph'):
        """
        Adds a new paragraph element.
        """
        self._currentElement.draw_parapraph(text, self._styles[style])
