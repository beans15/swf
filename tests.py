# -*- coding: utf-8 -*-

import unittest

import datatypes


class DataTypesTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_parse_rect(self):
        rect = datatypes.Rect('\x70\x00\x09\x60\x00\x00\x96\x00')
        assert rect.x_min == 0
        assert rect.x_max == 240
        assert rect.y_min == 0
        assert rect.y_max == 240
        assert rect.tell() == 8, 'Got: %d' % rect.tell()
