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


class StyleLibrary:

    def __init__(self, base_style=None, unit=mm):
        self._styles = {}
        self._unit = unit
        if base_style is not None and base_style.validate() is False:
            base_style.inherit(self._base_style)

        self.define('base', base_style or self._base_style)
        self._defines_base_styles()

    def define(self, stylename, style):
        """
        Add a new style
        """
        if hasattr(style, 'text_indent') is True:
            style.text_indent *= self._unit
        self._styles[stylename] = style

    def get(self, stylename, inherits=None):
        """
        Gets a style by his name and inherits from other styles

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

    def list(self):
        """
        Returns a list with all the styles names
        """
        return self._styles.keys()

    @property
    def _base_style(self):
        """
        Create and return a Style object with the default values
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

    def _defines_base_styles(self):
        """
        Create and return a bunch of basic styles
        """
        self.define('paragraph', Style())

    add = define  # Alias for the define method
