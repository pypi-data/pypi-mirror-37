#!/usr/bin/python

from helper.grab import grab
import unittest

class TestM1(unittest.TestCase):
    def test_grab(self):
        try:
           l = grab('test_html.html')
        except Exception, err:
           raise IOError("Test html test_html.html is not accesible")
        self.assertEqual(l, '<DOCTYP!>')

