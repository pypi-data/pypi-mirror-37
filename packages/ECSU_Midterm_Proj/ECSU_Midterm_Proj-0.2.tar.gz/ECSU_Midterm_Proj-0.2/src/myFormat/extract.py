#!usr/bin/python2.7
"""This extract module uses python regular expression to extract data from the link to a csv file.
"""
from sub.m1 import url_html_data
from sub.m2 import write_to_csv

__author__ = "Disaiah Bennett"
__version__ = "1.0"

def main():
    """Extract data from the ECSU url with python regex, and place the data into a csv file.
    """
    url = 'http://www.ecsu.edu/faculty-staff/profiles/index.html'

    tr_head, tr_name, tr_department, tr_email, tr_number = url_html_data(url)
    _ = write_to_csv(tr_head, tr_name, tr_department, tr_email, tr_number)

    for i in range(len(tr_email)):
        print tr_name[i], tr_department[i], tr_email[i], tr_number[i]

if __name__ == '__main__':
    main()
