# -*- coding: utf-8 -*-
"""
affinitic.pdf
-------------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

import copy
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle


class Style(object):
    _accepted_attrs = (
        'color',
        'text_align',
        'text_indent',
        'text_transform',
        'font_family',
        'font_size',
        'font_style',
        'background_color',
        'border_color',
        'width',
        'height',
        'line_height',
    )
    _mandatory_attrs = (
    )
    _paragraph_styles_match = {
        '_color': 'textColor',
        '_text_align': 'alignment',
        'text_indent': 'leftIndent',
        '_text_transform': 'textTransform',
        'font_family': 'fontName',
        'font_size': 'fontSize',
        '_line_height': 'leading',
    }

    def __init__(self, **kwargs):
        self._inherits = []
        for arg in kwargs:
            if arg not in self._accepted_attrs:
                raise ValueError(
                    "Unknown argument '%s' for Style object" % arg)
            setattr(self, arg, kwargs[arg])

    def copy(self):
        """Return a copy of the current object"""
        return copy.deepcopy(self)

    def inherit(self, *styles):
        """Inherits from multiple styles objects"""
        for style in styles:
            self._inherit(style)

    def _inherit(self, style):
        """
        Update the current style by inheriting of the given style for the
        undefined properties
        """
        self._inherits.append(style)
        for property_name in style.__dict__:
            if hasattr(self, property_name) is False or \
               hasattr(self, property_name) is True and \
               getattr(self, property_name) is None:
                setattr(self, property_name, getattr(style, property_name))

    def inherited_property(self, name):
        """Return the inherited values for the given property name"""
        return [getattr(i, name) for i in self._inherits
                if hasattr(i, name)]

    def validate(self):
        """Verify if all the mandatory attributes are defined"""
        for attr in self._mandatory_attrs:
            if hasattr(self, attr) is False or getattr(self, attr) is None:
                raise ValueError("The attribute '%s' is mandatory on '%s'"
                                 % (attr, self.__class__))

    @property
    def paragraph_style(self):
        """
        Return a ParagraphStyle object that match to the current style
        attributes
        """
        style = ParagraphStyle('style')
        for key in self._paragraph_styles_match:
            setattr(style, self._paragraph_styles_match[key],
                    getattr(self, key))
        return style

    @property
    def _text_align(self):
        """Parse the text_align property"""
        align_dict = {
            'LEFT': TA_LEFT,
            'CENTER': TA_CENTER,
            'RIGHT': TA_RIGHT,
            'JUSTIFY': TA_JUSTIFY,
        }
        if self.text_align.upper() not in align_dict.keys():
            raise ValueError("Unknown value '%s' for the text_align "
                             u"property" % self.text_align)
        return align_dict[self.text_align.upper()]

    @property
    def _text_transform(self):
        """Parse the text_transform property"""
        transform_dict = {
            'UPPERCASE': 'uppercase',
            'LOWERCASE': 'lowercase',
        }
        if self.text_transform is None:
            return
        if self.text_transform.upper() not in transform_dict.keys():
            raise ValueError(u"Unknow value '%' for the text_transform "
                             u"property" % self.text_transform)
        return transform_dict[self.text_transform.upper()]

    @property
    def _line_height(self):
        """Return the line_height property or 120% of font_size"""
        if self.line_height is None:
            return self.font_size * 1.2
        return self.line_height

    @property
    def _color(self):
        """Return the CYMK color for the color attribute"""
        return self.color.cmyk


class TableStyle(Style):
    _accepted_attrs = Style._accepted_attrs + (
        'border',
    )
    _mandatory_attrs = Style._mandatory_attrs + (
        'border',
        'border_color',
    )


class ColumnStyle(Style):
    _mandatory_attrs = Style._mandatory_attrs + (
        'width',
    )


class RowStyle(Style):
    _accepted_attrs = Style._accepted_attrs + (
        'border',
    )
    _mandatory_attrs = Style._mandatory_attrs + (
        'height',
    )
