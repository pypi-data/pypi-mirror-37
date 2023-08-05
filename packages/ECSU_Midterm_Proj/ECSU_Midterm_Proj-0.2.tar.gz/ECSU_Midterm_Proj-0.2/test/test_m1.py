#!usr/bin/python2.7
"""Unittest for module 1
"""
import unittest
from re import findall
from urllib import urlopen
from midterm.src.myFormat.sub.m1 import url_html_data

__author__ = "Disaiah Bennett"
__version__ = "1.0"

URL = 'http://www.ecsu.edu/faculty-staff/profiles/index.html'
PAGE = urlopen(URL)
DATA = PAGE.read()

HEADER = findall(r'<th>(.*?)</th>', DATA)
NAME = findall(r'l">(.*?)</a></td>', str(DATA))
DEPARTMENT = findall(r'<td>(.*?)<', str(DATA))
EMAIL = findall(r'a href="mailto:(.*?)">', str(DATA))
NUMBER = findall(r'a href="tel:(.*?)">', str(DATA))

class TestStringMethods(unittest.TestCase):
    """Unittest for module 1
    """
    def test_url_header001(self):
        """Test Module 001
        """
        self.trhead, _, _, _, _ = url_html_data(URL)
        try:
            self.assertEqual(self.trhead, HEADER)
        except IOError:
            pass
    def test_url_name002(self):
        """Test Module 002
        """
        _, self.trname, _, _, _ = url_html_data(URL)
        try:
            self.assertEqual(self.trname, NAME)
        except IOError:
            pass

    def test_url_department003(self):
        """Test Module 003
        """
        _, _, self.trdepart, _, _ = url_html_data(URL)
        try:
            self.assertEqual(self.trdepart, DEPARTMENT)
        except IOError:
            pass

    def test_url_email_004(self):
        """Test Module 004
        """
        _, _, _, self.tremail, _ = url_html_data(URL)
        try:
            self.assertEqual(self.tremail, EMAIL)
        except IOError:
            pass

    def test_url_number005(self):
        """Test Module 005
        """
        _, _, _, _, self.trnumber = url_html_data(URL)
        try:
            self.assertEqual(self.trnumber, NUMBER)
        except IOError:
            pass

if __name__ == '__main__':
    unittest.main()
