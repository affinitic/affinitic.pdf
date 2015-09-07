# -*- coding: utf-8 -*-
"""
affinitic.pdf
-------------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from reportlab.lib.colors import CMYKColor, Color, rgb2cmyk


class ColorRGB:

    def __init__(self, r=0, g=0, b=0, alpha=100):
        self.red = float(r)
        self.green = float(g)
        self.blue = float(b)
        self.alpha = float(alpha) / 100

    @property
    def cmyk(self):
        """
        Returns an CMYKColor for the current color
        """
        cmyk = rgb2cmyk(self.red / 255, self.green / 255, self.blue / 255)
        return CMYKColor(cmyk[0], cmyk[1], cmyk[2], cmyk[3], alpha=self.alpha)

    @property
    def rgb(self):
        """
        Returns an CMYKColor for the current color
        """
        return Color(
            self.red / 255,
            self.green / 255,
            self.blue / 255,
            alpha=self.alpha)
