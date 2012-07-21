# -*- coding: utf-8 -*-
"""
Created by mpeeters.
Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by NetExpe sprl
"""

from reportlab.lib.colors import PCMYKColor
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle


class BasicStyles(object):

    def __init__(self, base_color=PCMYKColor(0, 0, 0, 100)):
        self.base_color = base_color
        self.styles = {}

    def _define_basic_styles(self):
        """
        Creates the basic styles
        """
        self.styles.update({
            'paragraph': ParagraphStyle(
                name='paragraph',
                fontName='Helvetica',
                fontSize=10,
                leading=12,
                alignment=TA_JUSTIFY,
                textcolor=self.base_color),
            })
