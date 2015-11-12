# -*- coding: utf-8 -*-
"""
affinitic.pdf
-------------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from reportlab.graphics.barcode.widgets import BarcodeCode128
from reportlab.graphics.shapes import Drawing
from reportlab.platypus import Flowable, Paragraph

from affinitic.pdf.cursor import Cursor
from affinitic.pdf.tools import ColorRGB


def add_element(me):

    def wrapper(*args, **kwargs):
        flowable = args[0]
        flowable._elements.append({
            'method': me,
            'args': args,
            'kwargs': kwargs,
            'position': flowable.cursor.real_position,
        })

    return wrapper


class ExtendedFlowable(Flowable, object):

    def __init__(self, measure_unit):
        super(ExtendedFlowable, self).__init__()
        self.unit = measure_unit
        self.cursor = Cursor()
        self._elements = []

    def draw(self):
        """Draw the elements"""
        for element in self._elements:
            position = element['position']
            if self._elements.index(element) > 0:
                last_position = self._elements[
                    self._elements.index(element) - 1]['position']
                self.cursor.move(x=position.x - last_position.x,
                                 y=position.y - last_position.y)
            else:
                self.cursor.move_to(x=position.x, y=position.y)
            element['method'](*element['args'], **element['kwargs'])

    def drawOn(self, canvas, *args, **kwargs):
        Flowable.drawOn(self, canvas, *args, **kwargs)

    @add_element
    def draw_string(self, *args, **kwargs):
        return self._draw_string(*args, **kwargs)

    def _draw_string(self, value=''):
        """
        Use the flowable drawString methods to add a string on the current
        cursor position
        """
        self.canv.drawString(
            self.cursor.x * self.unit,
            self.cursor.y * self.unit,
            value)

    @add_element
    def draw_paragraph(self, *args, **kwargs):
        return self._draw_paragraph(*args, **kwargs)

    def _draw_paragraph(self, text, style, **kwargs):
        """Draw a paragraph"""
        paragraph_style = style.paragraph_style
        p_width, p_height = self._get_paragraph_size(style, **kwargs)

        canvas = self.canv
        paragraph = Paragraph(text, paragraph_style)
        width, height = paragraph.wrapOn(
            self.canv, p_width, p_height)

        if kwargs.get('debug', False) is True:
            paragraph_style.borderWidth = 1
            paragraph_style.borderColor = ColorRGB(0, 0, 0, alpha=50).rgb

        y_pos = self.cursor.y - style.padding_top - style.space_before
        paragraph.drawOn(
            canvas,
            self.cursor.x * self.unit,
            y_pos * self.unit - height,
        )

        self.cursor.move(y=height / self.unit + style.padding_v)
        if height < p_height:
            self.cursor.move(y=(p_height - height) / self.unit)

    def _get_paragraph_size(self, style, **kwargs):
        """Return the paragraph width and height"""
        if 'width' not in kwargs.keys() or kwargs['width'] is None:
            paragraph_width = self._frame.width - (self.cursor.x * self.unit)
        else:
            paragraph_width = kwargs['width'] * self.unit

        if 'height' not in kwargs.keys() or kwargs['height'] is None:
            paragraph_height = 0
        else:
            paragraph_height = kwargs['height'] * self.unit

        return paragraph_width, paragraph_height

    @add_element
    def draw_rectangle(self, *args, **kwargs):
        return self._draw_rectangle(*args, **kwargs)

    def _draw_rectangle(
            self,
            width,
            height,
            bg_color=None,
            stroke_color=None,
            fill=0,
            stroke=0):
        """Draw a rectangle"""
        if stroke:
            self.canv.setStrokeColor(stroke_color.rgb)
        if fill:
            self.canv.setFillColor(bg_color.rgb)
        self.canv.rect(
            self.cursor.x * self.unit,
            self.cursor.y * self.unit - height * self.unit,
            width * self.unit + 0.3,
            height * self.unit + 0.3,
            fill=fill,
            stroke=stroke,
        )

    @add_element
    def draw_grid(self, *args, **kwargs):
        return self._draw_grid(*args, **kwargs)

    def _draw_grid(
            self,
            size,
            width,
            height,
            color=ColorRGB(r=150, g=150, b=150)):
        """Draw the grid"""
        self._draw_rectangle(width, height, stroke_color=color)
        for x in range(int(width) / size):
            self.cursor.move(x=size)
            self._draw_v_line(height, color=color)
        self.cursor.move_to(x=0)
        for y in range(int(height) / size):
            self.cursor.move(y=size)
            self._draw_h_line(width, color=color)

    @add_element
    def draw_h_line(self, *args, **kwargs):
        return self._draw_h_line(*args, **kwargs)

    def _draw_h_line(self, width, color=ColorRGB(r=150, g=150, b=150)):
        """Draw an horizontal line"""
        self.canv.setStrokeColor(color.rgb)
        self.canv.line(
            self.cursor.x * self.unit,
            self.cursor.y * self.unit,
            (self.cursor.x + width) * self.unit,
            self.cursor.y * self.unit)

    @add_element
    def draw_v_line(self, *args, **kwargs):
        return self._draw_h_line(*args, **kwargs)

    def _draw_v_line(self, height, color=ColorRGB(r=150, g=150, b=150)):
        """Draw a vertical line"""
        self.canv.setStrokeColor(color.rgb)
        self.canv.line(
            self.cursor.x * self.unit,
            self.cursor.y * self.unit,
            self.cursor.x * self.unit,
            (self.cursor.y - height) * self.unit)

    @add_element
    def draw_barcode(self, *args, **kwargs):
        return self._draw_barcode(*args, **kwargs)

    def _draw_barcode(self, value):
        """Draw a barcode"""
        barcode = Drawing()
        barcode.add(BarcodeCode128(value=value, barWidth=0.75))
        barcode.drawOn(
            self.canv,
            self.cursor.x * self.unit,
            self.cursor.y * self.unit,
        )


class SimulationFlowable(ExtendedFlowable):

    def __init__(self, measure_unit, document):
        Flowable.__init__(self)
        self.unit = measure_unit
        self.cursor = Cursor()
        self._elements = []
        self.canv = document.canv
        self._frame = document.pageTemplate.frames[0]

    def draw(self):
        return

    def drawOn(self, *args, **kwargs):
        return

    def paragraph_size(self, text, style, **kwargs):
        """Return the simulated paragraph final size"""
        paragraph_style = style.paragraph_style
        p_width, p_height = self._get_paragraph_size(style, **kwargs)
        paragraph = Paragraph(text, paragraph_style)
        width, height = paragraph.wrapOn(self.canv, p_width, p_height)
        return (
            width / self.unit,
            height / self.unit,
        )
