#system modules
import csv, sys, json, io
#custom modules
from io_utilities.base_exportData import base_exportData
#third party modules
try:
    import pyopenms
except ImportError as e:
    print(e)

class smartPeak_o(base_exportData):
    """a class to export data"""

    def store_mzML(self, out, output):
        """
        Store as mzML File

        Args:
            out (str): out filename
            output (): chromatogram object
        """

        pyopenms.MzMLFile().store(out, output)