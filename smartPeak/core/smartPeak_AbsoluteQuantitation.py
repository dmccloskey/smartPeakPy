# -*- coding: utf-8 -*-
# #modules
from smartPeak.pyTOPP.OpenSwathFeatureXMLToTSV import OpenSwathFeatureXMLToTSV
# 3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)
    

class smartPeak_AbsoluteQuantitation():
    def __init__(self):
        self.unknowns = None
        self.quantitationMethods = None
        self.quantitationStandards = None

    def clear_data(self):
        self.unknowns = None
        self.quantitationMethods = None
        self.quantitationStandards = None

    def load_quantitationMethods(
        self,
        filenames_I,
        verbose_I=False
    ):
        """Load AbsoluteQuantitationMethods

        Args:
            filenames_I (dict): dictionary of filename strings

        Internals:
            quantitationMethods (list): list of AbsoluteQuantitationMethod objects

        """
        if verbose_I:
            print("loading quantitation methods")

        quantitationMethods_csv_i = None
        if 'quantitationMethods_csv_i'in filenames_I.keys():
            quantitationMethods_csv_i = filenames_I['quantitationMethods_csv_i']

        quantitationMethods = []
        aqmf = pyopenms.AbsoluteQuantitationMethodFile()
        aqmf.load(quantitationMethods_csv_i, quantitationMethods)
        self.quantitationMethods = quantitationMethods

    def store_quantitationMethods(
        self,
        filenames_I
    ):
        """ """
        pass

    def load_quantitationStandards(
        self,
        filenames_I
    ):
        """Load AbsoluteQuantitationStandardss

        Args:
            filenames_I (dict): dictionary of filename strings

        Internals:
            quantitationStandards (list): list of AbsoluteQuantitationStandards objects

        """
        quantitationStandards_csv_i = None
        if 'quantitationStandards_csv_i'in filenames_I.keys():
            quantitationStandards_csv_i = filenames_I['quantitationStandards_csv_i']

    def quantifyComponents(self, verbose_I=False):
        """Quantify all unknown samples based on the quantitationMethod
        
        Args:
            unknowns (list): list of FeatureMaps to quantify
            
        """        
        if verbose_I:
            print("Quantifying features")

        aq = pyopenms.AbsoluteQuantitation()
        aq.setQuantMethods(self.quantitationMethods)
        aq.quantifyComponents(self.unknowns)

    def setUnknowns(self, unknowns):
        """Set unknown featureMaps
        
        Args:
            unknowns (FeatureMap): FeatureMap to quantify
            
        """
        self.unknowns = unknowns

    def getUnknowns(self):
        """Set unknown featureMaps
        
        Returns:
            FeatureMap: unknowns: FeatureMaps that was quantified
            
        """
        return self.unknowns
