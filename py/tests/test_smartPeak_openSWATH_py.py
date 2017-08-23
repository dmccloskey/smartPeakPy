# -*- coding: utf-8 -*-
#utilities
import copy
#modules
from .smartPeak import smartPeak
from .smartPeak_i import smartPeak_i
from .pyTOPP.MRMMapper import MRMMapper
from .pyTOPP.OpenSwathChromatogramExtractor import OpenSwathChromatogramExtractor
from .pyTOPP.OpenSwathRTNormalizer import OpenSwathRTNormalizer
from .pyTOPP.OpenSwathFeatureXMLToTSV import OpenSwathFeatureXMLToTSV
from .pyTOPP.MRMFeatureFilter import MRMFeatureFilter
from .pyTOPP.MRMFeatureSelector import MRMFeatureSelector
from .pyTOPP.MRMFeatureValidator import MRMFeatureValidator
from .data.ReferenceDataMethods import ReferenceDataMethods
#3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)
import pytest

class test_smartPeak_openSWATH_py():
    """tests for smartPeak_openSWATH_py
    
    TODO: 
    1. make test files
    2. add method body code
    3. test
    """

    def test_load_TraML(self,verbose_I=False):
        """tests for load_TraML function
        """
        pass