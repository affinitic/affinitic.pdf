# -*- coding: utf-8 -*-
"""
affinitic.pdf
-------------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

import unittest2

from affinitic.pdf.style import Style, StyleLibrary
from affinitic.pdf.tools import ColorRGB


class TestStyle(unittest2.TestCase):

    @property
    def _base_style(self):
        """
        Creates and return a basic style where all attributes are defined
        """
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
        Tests Style.__init__(self, **kwargs) with accepted keyword arguments
        """
        style = Style(text_align='center', font_size=8)

        self.assertEquals('center', style.text_align)
        self.assertEquals(8, style.font_size)

    def test_init_refused_arguments(self):
        """
        Tests Style.__init__(self, **kwargs) with refused keyword arguments
        """
        self.assertRaises(ValueError, Style, foo='bar')

    def test_copy(self):
        """ Tests Style.copy(self) """
        style1 = Style(text_align='center')
        style2 = style1.copy()
        style2.text_align = 'right'

        self.assertEquals('center', style1.text_align)
        self.assertEquals('right', style2.text_align)

    def test_inherit(self):
        """ Tests Style.inherit(self, style) """
        style1 = Style(text_align='center')
        style2 = Style(text_align='right', font_size=10)
        style1.inherit(style2)

        self.assertEquals('center', style1.text_align)
        self.assertEquals(10, style1.font_size)

    def test_validate(self):
        """ Tests Style.validate(self) """
        style1 = self._base_style.copy()
        style1.color = None

        self.assertEquals(False, style1.validate())
        self.assertEquals(True, self._base_style.validate())

    def test_paragraph_style_property_known_value(self):
        """ Tests Style.paragraph_style """
        from reportlab.lib.styles import ParagraphStyle

        paragraph_style = self._base_style.paragraph_style

        self.assertTrue(isinstance(paragraph_style, ParagraphStyle))
        self.assertEquals(9, paragraph_style.fontSize)
        self.assertEquals('Helvetica', paragraph_style.fontName)

    def test_text_align_property(self):
        """ Tests Style._text_align """
        style1 = Style(text_align='center')
        style2 = Style(text_align='foo')

        self.assertEquals(1, style1._text_align)
        self.assertRaises(ValueError, lambda: style2._text_align)

    def test_text_transform_property(self):
        """ Tests Style._text_transform """
        style1 = Style(text_transform='Uppercase')
        style2 = Style(text_transform='foo')
        style3 = Style(text_transform=None)

        self.assertEquals('uppercase', style1._text_transform)
        self.assertRaises(ValueError, lambda: style2._text_transform)
        self.assertEquals(None, style3._text_transform)

    def test_line_height_property(self):
        """ Tests Style._line_height """
        style1 = Style(line_height=10, font_size=9)
        style2 = Style(line_height=None, font_size=10)

        self.assertEquals(10, style1._line_height)
        self.assertEquals(12, style2._line_height)

    def test_color_property(self):
        """ Tests Style._color """
        from reportlab.lib.colors import CMYKColor

        style = Style(color=ColorRGB(0, 0, 0))

        self.assertTrue(isinstance(style._color, CMYKColor))
        self.assertEquals(0, style._color.blue)
        self.assertEquals(0, style._color.green)
        self.assertEquals(0, style._color.yellow)
        self.assertEquals(1, style._color.black)


class TestStyleLibrary(unittest2.TestCase):

    def test_init_without_base(self):
        """ Tests StyleLibrary.__init__(self, base_style=None, unit=mm) """
        from reportlab.lib.units import mm

        lib = StyleLibrary()

        self.assertEquals(mm, lib._unit)
        self.assertEquals(1, len(lib._styles.keys()))
        self.assertEquals('base', lib._styles.keys()[0])
        self.assertEquals(9, lib._styles['base'].font_size)

    def test_init_with_base(self):
        """ Tests StyleLibrary.__init__(self, base_style=None, unit=mm) """
        base = Style(font_size=12)
        self.assertFalse(hasattr(base, 'text_indent'))

        lib = StyleLibrary(base_style=base)

        self.assertEquals(1, len(lib._styles.keys()))
        self.assertEquals('base', lib._styles.keys()[0])
        self.assertEquals(12, lib._styles['base'].font_size)
        self.assertEquals(0, lib._styles['base'].text_indent)

    def test_define(self):
        """ Tests StyleLibrary.define(self, stylename, style) """
        from reportlab.lib.units import mm

        style = Style(font_size=10, text_indent=1)
        lib = StyleLibrary()
        lib.define('test', style)

        self.assertEquals(2, len(lib._styles.keys()))
        self.assertEquals(sorted(['base', 'test']), sorted(lib._styles.keys()))
        self.assertEquals(mm, lib._styles['test'].text_indent)

    def test_get_no_inherits(self):
        """ Tests StyleLibrary.get(self, stylename, inherits=None) """
        style = Style(font_size=10)
        lib = StyleLibrary()
        lib.define('test', style)

        result = lib.get('test')

        self.assertEquals(10, result.font_size)
        self.assertEquals('Helvetica', result.font_family)  # Inherited

    def test_get_single_inherit(self):
        """ Tests StyleLibrary.get(self, stylename, inherits=None) """
        style1 = Style(font_size=10)
        style2 = Style(font_size=12, text_align='center')
        lib = StyleLibrary()
        lib.define('test1', style1)
        lib.define('test2', style2)

        result = lib.get('test1', inherits=['test2'])

        self.assertEquals(10, result.font_size)
        # Inherited from test2
        self.assertEquals('center', result.text_align)
        # Inherited from base
        self.assertEquals('Helvetica', result.font_family)

    def test_get_multiple_inherits(self):
        """ Tests StyleLibrary.get(self, stylename, inherits=None) """
        style1 = Style(font_size=10)
        style2 = Style(font_size=11, text_align='center')
        style3 = Style(font_size=12, text_align='right',
            text_transform='uppercase')
        lib = StyleLibrary()
        lib.define('test1', style1)
        lib.define('test2', style2)
        lib.define('test3', style3)

        result = lib.get('test1', inherits=['test2', 'test3'])

        self.assertEquals(10, result.font_size)
        # Inherited from test2
        self.assertEquals('center', result.text_align)
        # Inherited from test3
        self.assertEquals('uppercase', result.text_transform)
        # Inherited from base
        self.assertEquals('Helvetica', result.font_family)

    def test_list(self):
        """ Tests StyleLibrary.list(self) """
        lib = StyleLibrary()
        self.assertEquals(lib.list(), lib._styles.keys())

    def test_base_style_property(self):
        """ Tests StyleLibrary._base_style """
        from affinitic.pdf.tools import ColorRGB

        lib = StyleLibrary()

        self.assertEquals(ColorRGB(0, 0, 0).red, lib._base_style.color.red)
        self.assertEquals(ColorRGB(0, 0, 0).green, lib._base_style.color.green)
        self.assertEquals(ColorRGB(0, 0, 0).blue, lib._base_style.color.blue)
        self.assertEquals('left', lib._base_style.text_align)
        self.assertEquals(0, lib._base_style.text_indent)
        self.assertEquals(None, lib._base_style.text_transform)
        self.assertEquals('Helvetica', lib._base_style.font_family)
        self.assertEquals(9, lib._base_style.font_size)
        self.assertEquals('normal', lib._base_style.font_style)
        self.assertEquals(None, lib._base_style.background_color)
        self.assertEquals(None, lib._base_style.border_color)
        self.assertEquals(None, lib._base_style.width)
        self.assertEquals(None, lib._base_style.height)
        self.assertEquals(None, lib._base_style.line_height)
