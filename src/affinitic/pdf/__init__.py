# -*- coding: utf-8 -*-
"""
affinitic.pdf
-------------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

from affinitic.pdf.element import DeferredElement
from affinitic.pdf.element import Footer
from affinitic.pdf.element import Header
from affinitic.pdf.pdf import Pdf
from affinitic.pdf.tools import ColorRGB

from affinitic.pdf.style import ColumnStyle
from affinitic.pdf.style import RowStyle
from affinitic.pdf.style import Style
from affinitic.pdf.style import StyleLibrary
from affinitic.pdf.style import TableStyle


__all__ = (
    ColorRGB.__name__,
    DeferredElement.__name__,
    Footer.__name__,
    Header.__name__,
    Pdf.__name__,
    # Style
    ColumnStyle.__name__,
    RowStyle.__name__,
    Style.__name__,
    StyleLibrary.__name__,
    TableStyle.__name__,
)
