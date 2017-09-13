# -*- coding: utf-8 -*-
# #modules
# from .smartPeak import smartPeak
#3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)

class smartPeak_AbsoluteQuantitation_py():
    def __init__(self):
        self.unknowns = None
        self.quantitationMethods = None
        self.quantitationStandards = None

    def load_quantitationMethods(self,
        filenames_I):
        """Load AbsoluteQuantitationMethods

        Args:
            filenames_I (list): list of filename strings

        Internals:
            quantitationMethods (list): list of AbsoluteQuantitationMethod objects

        """
        quantitationMethods_csv_i = None
        if 'quantitationMethods_csv_i'in filenames_I.keys(): quantitationMethods_csv_i = filenames_I['quantitationMethods_csv_i']

        quantitationMethods = []
        aqmf = pyopenms.AbsoluteQuantitationMethodFile()
        aqmf.load(quantitationMethods_csv_i, quantitationMethods)
        self.quantitationMethods = quantitationMethods

    def store_quantitationMethods(self,
        filenames_I):
        """ """
        pass

    def load_quantitationStandards(self,
        filenames_I):
        """Load AbsoluteQuantitationStandardss

        Args:
            filenames_I (list): list of filename strings

        Internals:
            quantitationStandards (list): list of AbsoluteQuantitationStandards objects

        """
        quantitationStandards_csv_i = None
        if 'quantitationStandards_csv_i'in filenames_I.keys(): quantitationStandards_csv_i = filenames_I['quantitationStandards_csv_i']

        pass

    def quantifyComponents(self):
        """Quantify all unknown samples based on the quantitationMethod
        
        Args:
            unknowns (list): list of FeatureMaps to quantify
            
        """
        aq = pyopenms.AbsoluteQuantitation()
        aq.setQuantMethods(self.quantitationMethods)
        aq.quantifyComponents(self.unknowns)

    def setUnknowns(self, unknowns):
        self.unknowns = unknowns

    def getUnknowns(self, unknowns):
        return self.unknowns
