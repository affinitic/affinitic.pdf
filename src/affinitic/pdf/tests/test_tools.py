# -*- coding: utf-8 -*-
"""
affinitic.pdf
-------------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

import unittest2

from affinitic.pdf import tools


class TestColorRGB(unittest2.TestCase):

    def test_cmyk(self):
        color = tools.ColorRGB(r=255, g=255, b=255, alpha=100)
        cmyk = color.cmyk
        self.assertEqual(0, cmyk.cyan)
        self.assertEqual(0, cmyk.magenta)
        self.assertEqual(0, cmyk.yellow)
        self.assertEqual(0, cmyk.black)
        self.assertEqual(1.0, cmyk.alpha)

    def test_rgb(self):
        color = tools.ColorRGB(r=255, g=255, b=255, alpha=100)
        rgb = color.rgb
        self.assertEqual(1.0, rgb.red)
        self.assertEqual(1.0, rgb.green)
        self.assertEqual(1.0, rgb.blue)
        self.assertEqual(1.0, rgb.alpha)
