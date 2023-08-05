#!usr/bin/python2.7
"""Unit test for module 2
"""
import unittest
from midterm.src.myFormat.sub.m2 import write_to_csv
from midterm.src.myFormat.sub.m1 import url_html_data

__author__ = "Disaiah Bennett"
__version__ = "1.0"

TEST_FILE = "test_file.csv"

URL = 'http://www.ecsu.edu/faculty-staff/profiles/index.html'
HEADER, NAME, DEPARTMENT, EMAIL, NUMBER = url_html_data(URL)

class TestExtractMethods(unittest.TestCase):
    """Unittest for module 2
    """
    def test_write_to_csv001(self):
        """Test Module 006
        """
        try:
            self.csv_file = write_to_csv(HEADER, NAME, DEPARTMENT, EMAIL, NUMBER)
        except IOError:
            pass
        try:
            self.file_ = open(TEST_FILE, "r")
            self.data = self.file_.read()
        except IOError:
            pass




if __name__ == '__main__':
    unittest.main()
