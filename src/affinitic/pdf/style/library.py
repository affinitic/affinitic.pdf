# -*- coding: utf-8 -*-
"""
affinitic.pdf
-------------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from reportlab.lib.units import mm

from affinitic.pdf.style.style import Style
from affinitic.pdf.tools import ColorRGB


class StyleLibrary(object):

    def __init__(self, base_style=None, unit=mm):
        self._styles = {}
        self._unit = unit
        base_style.inherit(self._base_style)

        self.define('base', base_style or self._base_style)
        self._defines_base_styles()

    def define(self, stylename, style, inherits=None):
        """Add a new style"""
        style.name = stylename
        if hasattr(style, 'text_indent') is True:
            style.text_indent *= self._unit
        inherits = inherits or []
        for inherit in inherits:
            style.inherit(self._styles.get(inherit))
        style.validate()
        self._styles[stylename] = style

    def get(self, stylename, inherits=None):
        """
        Get a style by his name and inherits from other styles

        Parameters
        ----------
         - stylename    (String)
         - inherits *   (List) List of style names sorted by inherit position
        * Optional
        """
        if stylename not in self._styles.keys():
            raise ValueError("Unknown style '%s'" % stylename)
        inherits = inherits or []
        inherits.append('base')
        style = self._styles[stylename].copy()
        for inherited_style in inherits:
            style.inherit(self._styles[inherited_style])
        return style

    def has_style(self, stylename):
        """Verify if the given stylename exist in the library"""
        return stylename in self._styles

    def list(self):
        """Return a list with all the styles names"""
        return self._styles.keys()

    @property
    def _base_style(self):
        """Create and return a Style object with the default values"""
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

    def _defines_base_styles(self):
        """Create and return a bunch of basic styles"""
        self.define('paragraph', Style())

    add = define  # Alias for the define method
