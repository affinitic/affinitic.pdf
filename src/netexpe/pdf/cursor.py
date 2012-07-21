# -*- coding: utf-8 -*-
"""
Created by mpeeters.
Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by NetExpe sprl
"""


class Cursor(object):

    def __init__(self, x=0, y=0, indent=0):
        self._position = Position(x, y)
        self._indent = indent

    def move(self, x=0, y=0):
        """
        Moves the cursor from the current position.
        """
        self._position.x += x
        self._position.y -= y

    def move_to(self, x=None, y=None):
        """
        Places the cursor to a specified position and reinitialize the
        indentation.
        """
        if x is not None:
            self._position.x = x
            self._indent = 0
        if y is not None:
            self._position.y = y * -1

    def indent(self, value):
        """
        Increase or decrease the current identation.
        """
        self._indent += value

    def indent_to(self, value):
        """
        Redefines the indentation.
        """
        self._indent = value

    @property
    def x(self):
        """
        Returns the current x position.
        """
        return self._position.x + self._indent

    @property
    def y(self):
        """
        Returns the current y position.
        """
        return self._posittion.y


class Position(object):
    """
    An object containing the x and y values of the cursor
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
