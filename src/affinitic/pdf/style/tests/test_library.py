# -*- coding: utf-8 -*-
"""
affinitic.pdf
-------------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from reportlab.lib.units import mm

import unittest2

from affinitic.pdf.tools import ColorRGB
from affinitic.pdf.style import Style
from affinitic.pdf.style import StyleLibrary


class TestStyleLibrary(unittest2.TestCase):

    @property
    def _default_styles(self):
        return ['base', 'paragraph', 'table']

    def test_init_without_base(self):
        """Test StyleLibrary.__init__(self, base_style=None, unit=mm)"""
        lib = StyleLibrary()

        self.assertEquals(mm, lib._unit)
        self.assertEqual(sorted(self._default_styles),
                         sorted(lib._styles.keys()))
        self.assertTrue('base' in lib._styles.keys())
        self.assertEquals(9, lib._styles['base'].font_size)

    def test_init_with_base(self):
        """Test StyleLibrary.__init__(self, base_style=None, unit=mm)"""
        base = Style(font_size=12)
        self.assertFalse(hasattr(base, 'text_indent'))

        lib = StyleLibrary(base_style=base)

        self.assertEqual(sorted(self._default_styles),
                         sorted(lib._styles.keys()))
        self.assertTrue('base' in lib._styles.keys())
        self.assertEquals(12, lib._styles['base'].font_size)
        self.assertEquals(0, lib._styles['base'].text_indent)

    def test_define(self):
        """Test StyleLibrary.define(self, stylename, style, inherits=None)"""
        style = Style(font_size=10, text_indent=1)
        lib = StyleLibrary()
        lib.define('test', style)

        styles = self._default_styles
        styles.append('test')
        self.assertEquals(sorted(styles),
                          sorted(lib._styles.keys()))
        test_style = lib.get('test')
        self.assertEquals(1, test_style.text_indent)
        self.assertEquals(mm, test_style._left_indent)

    def test_get_no_inherits(self):
        """Test StyleLibrary.get(self, stylename, inherits=None)"""
        style = Style(font_size=10)
        lib = StyleLibrary()
        lib.define('test', style)

        result = lib.get('test')

        self.assertEquals(10, result.font_size)
        self.assertEquals('Helvetica', result.font_family)  # Inherited

    def test_get_single_inherit(self):
        """Test StyleLibrary.get(self, stylename, inherits=None)"""
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
        """Test StyleLibrary.get(self, stylename, inherits=None)"""
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

    def test_get_none_existing_style(self):
        """Test StyleLibrary.get(self, stylename, inherits=None)"""
        lib = StyleLibrary()
        self.assertRaises(ValueError, lib.get, 'foo')

    def test_list(self):
        """Test StyleLibrary.list(self)"""
        lib = StyleLibrary()
        self.assertEquals(lib.list(), lib._styles.keys())

    def test_base_style_property(self):
        """Test StyleLibrary._base_style"""
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
