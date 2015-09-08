# -*- coding: utf-8 -*-
"""
affinitic.pdf
-------------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from reportlab.lib.colors import CMYKColor

import unittest2

from affinitic.pdf.style import Style
from affinitic.pdf.tools import ColorRGB


class TestStyle(unittest2.TestCase):

    @property
    def _base_style(self):
        """Create and return a basic style where all attributes are defined"""
        return Style(
            color=ColorRGB(0, 0, 0),
            text_align='left',
            text_indent=0,
            text_transform=None,
            font_family='Helvetica',
            font_size=9,
            font_style='normal',
            background_color=None,
            border_color=None,
            width=None,
            height=None,
            line_height=None)

    def test_init_accepted_arguments(self):
        """
        Test Style.__init__(self, **kwargs) with accepted keyword arguments
        """
        style = Style(text_align='center', font_size=8)

        self.assertEquals('center', style.text_align)
        self.assertEquals(8, style.font_size)

    def test_init_refused_arguments(self):
        """
        Test Style.__init__(self, **kwargs) with refused keyword arguments
        """
        self.assertRaises(ValueError, Style, foo='bar')

    def test_copy(self):
        """Test Style.copy(self)"""
        style1 = Style(text_align='center')
        style2 = style1.copy()
        style2.text_align = 'right'

        self.assertEquals('center', style1.text_align)
        self.assertEquals('right', style2.text_align)

    def test_inherit(self):
        """Test Style.inherit(self, *styles)"""
        style1 = Style(text_align='center')
        style2 = Style(text_align='right', font_size=10)
        style1.inherit(style2)
        style3 = Style(text_align='center', font_size=12)
        style1.inherit(style3)

        self.assertEquals('center', style1.text_align)
        self.assertEquals(10, style1.font_size)

    def test_multiple_inherit(self):
        """Test Style.inherit(self, *styles)"""
        style1 = Style(text_align='center')
        style2 = Style(text_align='right', font_size=10)
        style3 = Style(height=50, font_size=12)
        style4 = Style(width=100, height=100)
        style1.inherit(style2, style3, style4)

        self.assertEquals('center', style1.text_align)
        self.assertEquals(10, style1.font_size)
        self.assertEquals(50, style1.height)
        self.assertEquals(100, style1.width)

    def test_inherited_property(self):
        """Test Style.inherited_property(self, name)"""
        style1 = Style(text_align='center')
        style2 = Style(text_align='right', font_size=10)
        style3 = Style(text_align='center', font_size=12)
        style1.inherit(style2, style3)

        self.assertEquals(['right', 'center'],
                          style1.inherited_property('text_align'))
        self.assertEquals([10, 12], style1.inherited_property('font_size'))
        self.assertEquals('center', style1.text_align)
        self.assertEquals(10, style1.font_size)

    def test_validate(self):
        """Test Style.validate(self)"""
        style1 = self._base_style.copy()
        style1.color = None

        self.assertEquals(False, style1.validate())
        self.assertEquals(True, self._base_style.validate())

    def test_paragraph_style_property_known_value(self):
        """Test Style.paragraph_style"""
        from reportlab.lib.styles import ParagraphStyle

        paragraph_style = self._base_style.paragraph_style

        self.assertTrue(isinstance(paragraph_style, ParagraphStyle))
        self.assertEquals(9, paragraph_style.fontSize)
        self.assertEquals('Helvetica', paragraph_style.fontName)

    def test_text_align_property(self):
        """Test Style._text_align"""
        style1 = Style(text_align='center')
        style2 = Style(text_align='foo')

        self.assertEquals(1, style1._text_align)
        self.assertRaises(ValueError, lambda: style2._text_align)

    def test_text_transform_property(self):
        """Test Style._text_transform"""
        style1 = Style(text_transform='Uppercase')
        style2 = Style(text_transform='foo')
        style3 = Style(text_transform=None)

        self.assertEquals('uppercase', style1._text_transform)
        self.assertRaises(ValueError, lambda: style2._text_transform)
        self.assertEquals(None, style3._text_transform)

    def test_line_height_property(self):
        """Test Style._line_height"""
        style1 = Style(line_height=10, font_size=9)
        style2 = Style(line_height=None, font_size=10)

        self.assertEquals(10, style1._line_height)
        self.assertEquals(12, style2._line_height)

    def test_color_property(self):
        """Test Style._color"""
        style = Style(color=ColorRGB(0, 0, 0))

        self.assertTrue(isinstance(style._color, CMYKColor))
        self.assertEquals(0, style._color.blue)
        self.assertEquals(0, style._color.green)
        self.assertEquals(0, style._color.yellow)
        self.assertEquals(1, style._color.black)
