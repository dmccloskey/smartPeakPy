# -*- coding: utf-8 -*-
from smartPeak.io.FileReader import FileReader
from smartPeak.core.Utilities import Utilities
from smartPeak.io.FileReader import FileReader
from smartPeak.io.OpenSwathFeatureXMLToTSV import OpenSwathFeatureXMLToTSV
from smartPeak.pyTOPP.OpenSwathChromatogramExtractor import OpenSwathChromatogramExtractor
from smartPeak.pyTOPP.OpenSwathRTNormalizer import OpenSwathRTNormalizer
from smartPeak.algorithm.MRMFeatureSelector import MRMFeatureSelector
from smartPeak.algorithm.MRMFeatureValidator import MRMFeatureValidator
from smartPeak.ui.FeaturePlotter import FeaturePlotter
from smartPeak.data.ReferenceDataMethods import ReferenceDataMethods
# external
import copy
# 3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)


class FileReaderOpenMS(FileReader):

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