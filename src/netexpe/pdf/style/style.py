# -*- coding: utf-8 -*-
"""
Created by mpeeters.
Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by NetExpe sprl
"""

import copy
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm


class Style:
    _accepted_attrs = ('color', 'text_align', 'text_indent', 'text_transform',
        'font_family', 'font_size', 'font_style', 'background_color',
        'border_color', 'width', 'height', 'line_height')
    #_default_values = {
    #    'color': ColorRGB(0, 0, 0),
    #    'text_align': 'left',
    #    'text_indent': 0,
    #    'text_transform': None,
    #    'font_family': 'Helvetica',
    #    'font_size': 9,
    #    'font_style': 'normal',
    #    'background_color': None,
    #    'border_color': None,
    #    'width': None,
    #    'height': None,
    #    'line_height': None,
    #}
    _paragraph_styles_match = {
        '_color': 'textColor',
        '_text_align': 'alignment',
        'text_indent': 'leftIndent',
        '_text_transform': 'textTransform',
        'font_family': 'fontName',
        'font_size': 'fontSize',
        '_line_height': 'leading',
    }

    def __init__(self, name, **kwargs):
        self.name = name
        for arg in kwargs:
            if arg not in self._accepted_attrs:
                raise ValueError(
                    "Unknown argument '%s' for Style object" % arg)
            setattr(self, arg, kwargs[arg])

    #def update_default_values(self, base_style=None):
    #    """
    #    Updates the empty properties of the current style with the properties
    #    of a given style or the default values.
    #    """
    #    if base_style:
    #        base_style.validate_style()
    #    for key in self._accepted_attrs:
    #        if not hasattr(self, key) or \
    #           hasattr(self, key) and getattr(self, key) is None:
    #            if base_style:
    #                setattr(self, key, getattr(base_style, key))
    #            else:
    #                setattr(self, key, self._default_values[key])

    #def validate_style(self):
    #    """
    #    Verifies that all mandatory properties are defined.
    #    """
    #    valid = True
    #    for key in self._accepted_attrs:
    #        if not hasattr(self, key):
    #            valid = False
    #    if valid is False:
    #        self.update_default_values()

    def copy(self):
        """
        Returns a copy of the current object
        """
        return copy.deepcopy(self)

    def inherit(self, style):
        """
        Updates the current style by inheriting of the given style for the
        undefined properties
        """
        for property_name in style.__dict__:
            if hasattr(self, property_name) is False:
                setattr(self, property_name, getattr(style, property_name))

    @property
    def paragraph_style(self):
        """
        Returns a ParagraphStyle object that match to the current style
        attributes
        """
        style = ParagraphStyle(self.name)
        for key in self._paragraph_styles_match:
            setattr(style, self._paragraph_styles_match[key],
                getattr(self, key))
        return style

    @property
    def _text_align(self):
        """
        Parses the text_align property
        """
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
        """
        Parses the text_transform property
        """
        transform_dict = {
            'UPPERCASE': 'uppercase',
            'LOWERCASE': 'lowercase',
        }
        if self.text_transform is None:
            return
        if self.text_transform.upper() not in transform_dict.keys():
            raise ValueError(u"Unknow value '%' for the text_transform "
                u"property" % self.text_transform)
        return transform_dict[self.text_transform]

    @property
    def _line_height(self):
        """
        Returns the line_height property or 120% of font_size
        """
        if self.line_height is None:
            return self.font_size * 1.2
        return self.line_height

    @property
    def _color(self):
        """
        Returns the CYMK color for the color attribute.
        """
        return self.color.cmyk


class BasicStyles:

    def __init__(self, base_style=None, unit=mm):
        self._base_style = base_style or Style('base_style')
        self._unit = unit

        self.styles = {}
        self._define_basic_styles()

    def _define_basic_styles(self):
        """
        Creates the basic styles
        """
        self.add_style(self._base_style, name='paragraph')

    def add_style(self, style, name=None):
        """
        Adds a new style
        """
        style.update_default_values(base_style=self._base_style)
        style.text_indent *= self._unit
        self.styles.update({name or style.name: style})
