# -*- coding: utf-8 -*-
"""
affinitic.pdf
-------------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from affinitic.pdf.flowable import ExtendedFlowable


class DeferredElement(ExtendedFlowable):

    def __init__(self, pdf):
        self.pdf = pdf
        self.page_number = pdf.page_number
        super(DeferredElement, self).__init__(pdf._measure_unit)

    def _render(self):
        self.pdf._currentElement = self
        self.render()

    def render(self):
        pass


class Footer(DeferredElement):
    """Baseclass for footer elements"""


class Header(DeferredElement):
    """Baseclass for header elements"""
