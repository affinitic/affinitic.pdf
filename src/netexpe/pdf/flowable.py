# -*- coding: utf-8 -*-
"""
Created by mpeeters.
Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by NetExpe sprl
"""

from reportlab.platypus import Flowable, Paragraph

from netexpe.pdf.cursor import Cursor


class ExtendedFlowable(Flowable):

    def __init__(self, measure_unit):
        Flowable.__init__(self)
        self.unit = measure_unit
        self.cursor = Cursor()

    def draw_string(self, value=''):
        """
        Uses the flowable drawString methods to add a string on the current
        cursor position.
        """
        self.canv.drawString(
            self.cursor.x * self.unit,
            self.cursor.y * self.unit,
            value)

    def draw_parapraph(self, text, style, **kwargs):
        """
        Draws a paragraph.
        """
        if 'width' not in kwargs.keys():
            paragraph_width = self._frame.width - (self.cursor.x * self.unit)
        else:
            paragraph_width = kwargs['width'] * self.unit

        if 'height' not in kwargs.keys():
            paragraph_height = 0
        else:
            paragraph_height = kwargs['heigh'] * self.unit

        if 'canvas' not in kwargs.keys():
            canvas = self.canv
        else:
            canvas = kwargs['canvas']

        paragraph = Paragraph(text, style)
        width, height = paragraph.wrapOn(
            self.canv, paragraph_width, paragraph_height)

        paragraph.drawOn(
            canvas,
            self.cursor.x * self.unit,
            self.cursor.y * self.unit - height)

        self.cursor.move(y=height / self.unit)
