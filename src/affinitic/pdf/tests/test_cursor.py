# -*- coding: utf-8 -*-
"""
affinitic.pdf
-------------

Created by mpeeters
:copyright: (c) 2015 by Affinitic SPRL
:license: GPL, see LICENCE.txt for more details.
"""

import unittest2

from affinitic.pdf import cursor


class TestCursor(unittest2.TestCase):

    @property
    def cursor(self):
        return cursor.Cursor()

    def test_init(self):
        """Test Cursor.__init__(self, x=0, y=0, indent=0)"""
        cursor = self.cursor
        self.assertEqual(0, cursor._indent)
        self.assertEqual(0, cursor.x)
        self.assertEqual(0, cursor.y)

    def test_move(self):
        """Test Cursor.move(self, x=0, y=0)"""
        cursor = self.cursor
        cursor.move(x=10, y=20)
        self.assertEqual(10, cursor.x)
        self.assertEqual(-20, cursor.y)

    def test_move_to(self):
        """Test Cursor.move_to(self, x=None, y=None)"""
        cursor = self.cursor
        cursor.move(x=10, y=20)

        cursor.move_to(x=5)
        self.assertEqual(5, cursor.x)
        self.assertEqual(-20, cursor.y)

        cursor.move_to(y=10)
        self.assertEqual(5, cursor.x)
        self.assertEqual(-10, cursor.y)

        cursor.move_to(x=10, y=20)
        self.assertEqual(10, cursor.x)
        self.assertEqual(-20, cursor.y)

    def test_indent(self):
        """Test Cursor.indent(self, value)"""
        cursor = self.cursor
        cursor.indent(10)
        self.assertEqual(10, cursor.x)
        cursor.indent(10)
        self.assertEqual(20, cursor.x)

    def test_indent_to(self):
        """Test Cursor.indent_to(self, value)"""
        cursor = self.cursor
        cursor.indent_to(15)
        self.assertEqual(15, cursor.x)
        cursor.indent_to(5)
        self.assertEqual(5, cursor.x)

    def test_new_line(self):
        """Test Cursor.new_line(self)"""
        cursor = self.cursor
        cursor.indent(10)
        cursor.indent(20)
        cursor.new_line()
        self.assertEqual(0, cursor.x)

    def test_position(self):
        """Test Cursor.position"""
        cursor = self.cursor
        cursor.move_to(x=10, y=20)
        position = cursor.position
        self.assertEqual(10, position.x)
        self.assertEqual(-20, position.y)

    def test_real_position(self):
        """Test Cursor.real_position"""
        cursor = self.cursor
        cursor.move_to(x=10, y=20)
        position = cursor.real_position
        self.assertEqual(10, position.x)
        self.assertEqual(20, position.y)
