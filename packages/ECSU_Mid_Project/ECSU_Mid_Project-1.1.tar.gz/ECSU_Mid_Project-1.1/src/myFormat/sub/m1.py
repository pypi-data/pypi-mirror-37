#!usr/bin/python2.7
"""Retreives ecsu url link and return the faculty data within the table.
"""

__author__ = "Disaiah Bennett"
__version__ = "1.0"

from urllib import urlopen
import re

__author__ = "Disaiah Bennett"
__version__ = "1.0"

def url_html_data(url):
    """Retreives, extract, and returns url data with python regular expression.
        Returns:
            table_head: list - headers in the html table row.
            tr_name: string - table row facultly name.
            tr_department: string - table data department.
            tr_email: string - table data email.
            tr-number: string- table data phone number.
        Example:
            >>> fac_header, fac_name, fac_department, fac_email, fac_number = url_html_data(url)
    """
    page = urlopen(url)
    data = page.read()

    table_head = re.findall(r'<th>(.*?)</th>', data)
    tr_name = re.findall(r'l">(.*?)</a></td>', str(data))
    tr_department = re.findall(r'<td>(.*?)<', str(data))
    tr_email = re.findall(r'a href="mailto:(.*?)">', str(data))
    tr_number = re.findall(r'a href="tel:(.*?)">', str(data))

    return table_head, tr_name, tr_department, tr_email, tr_number
