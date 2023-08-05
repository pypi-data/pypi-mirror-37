#!usr/bin/python2.7
"""Write python regex data into csv file.
"""
import unicodecsv as csv

__author__ = "Disaiah Bennett"
__version__ = "1.0"

def write_to_csv(tr_head, tr_name, tr_department, tr_email, tr_number):
    """Writes extracted data to csv file.
        Returns:
            new_file: csv - new csv file.
        Example:
            >>> new_file = write_to_csv(tr_head, tr_name, tr_department, tr_email, tr_number)
    """
    new_file = csv.writer(open("ecsu_faculty.csv", "w"))
    new_file.writerow([tr_head[0], tr_head[1], tr_head[2], tr_head[3]])

    space = ""

    for i in range(len(tr_email)):
        for _ in range(len(tr_email)):
            if tr_department[i] == '':
                tr_department.remove(space)
            else:
                pass

    for i in range(len(tr_email)):
        new_file.writerow([tr_name[i], tr_department[i], tr_email[i], tr_number[i]])
    return new_file
