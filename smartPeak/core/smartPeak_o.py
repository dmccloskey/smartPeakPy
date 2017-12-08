# -*- coding: utf-8 -*-
# system modules
import csv
import sys
# third party modules
try:
    import pyopenms
except ImportError as e:
    print(e)

class smartPeak_o():
    """a class to export data"""

    def __init__(self, data_I=[]):
        if data_I: 
            self.add_data(data_I)
        else: 
            self.data = []

    def add_data(self, data_I):
        """add data"""
        self.data = data_I

    def clear_data(self):
        """clear existing data"""
        # del self.data[:]
        self.data = None

    def write_dict2csv(self, filename, headers=None):
        # write dict to csv
        with open(filename, 'w', newline='') as f:
            if headers: 
                fieldname = headers
            else: 
                fieldname = list(self.data[0].keys())
            writer = csv.DictWriter(f, fieldnames=fieldname)
            try:
                writer.writeheader()
                writer.writerows(self.data)
            except csv.Error as e:
                sys.exit(e)

    def store_mzML(self, out, output):
        """
        Store as mzML File

        Args:
            out (str): out filename
            output (): chromatogram object
        """

        pyopenms.MzMLFile().store(out, output)