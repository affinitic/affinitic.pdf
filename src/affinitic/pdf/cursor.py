# -*- coding: utf-8 -*-
"""
affinitic.pdf
-------------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""


class Cursor(object):

    def __init__(self, x=0, y=0, indent=0):
        self._position = Position(x, y)
        self._indent = indent

    def move(self, x=0, y=0):
        """Move the cursor from the current position"""
        self._position.x += x
        self._position.y += (y * -1)

    def move_to(self, x=None, y=None):
        """
        Places the cursor to a specified position and reinitialize the
        indentation
        """
        if x is not None:
            self._position.x = x
            self._indent = 0
        if y is not None:
            self._position.y = y * -1

    def indent(self, value):
        """Increase or decrease the current identation"""
        self._indent += value

    def indent_to(self, value):
        """Redefine the indentation"""
        self._indent = value

    def new_line(self):
        """Define a new line"""
        self._indent = 0

    @property
    def x(self):
        """Return the current x position"""
        return self._position.x + self._indent

    @property
    def y(self):
        """Return the current y position"""
        return self._position.y

    @property
    def position(self):
        """Return the current position"""
        return Position(self.x, self.y)

    @property
    def real_position(self):
        """Return the current position without the negative value for the y"""
        return Position(self.x, self.y * -1)


class Position(object):
    """An object containing the x and y values of the cursor"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
