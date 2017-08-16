#utilities
import copy
from math import log, exp, sqrt
#modules
from smartPeak.smartPeak import smartPeak
#3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)

class IsotopeLabeledQuantification():
    """Class for isotope labeled quantification
    """
    def __init__(self):
        self.standards = None
        self.unknowns = None
        self.calibration = None

    def load_standards(self,filenames):
        """Load processed featureMaps for calibration
        
        Args
            filenames (list(str)): list of featuremap filenames
        """
        pass

    def load_unknowns(self,filenames):
        """Load processed unknown samples for quantification
        
        Args
            filenames (list(str)): list of featuremap filenames
        """
        pass

    def load_quantitationMethod(self,filename):
        """Load quantitationMethod
        
        Args
            filename (str): name of the file
        """
        pass

    def import_calibration(self,filename):
        """Import calibration information

        Args
            filename (str): name of the file
        """
        pass

    def export_calibration(self,filename):
        """Export calibration information

        Args
            filename (str): name of the file
        """
        pass

    def calibrate(self):
        """Calculate the calibration curve for each compound

        """
        pass

    def apply_calibration(self):
        """apply_calibration to each unknown sample and compound

        """
        pass

      


