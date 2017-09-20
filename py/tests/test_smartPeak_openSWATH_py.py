# -*- coding: utf-8 -*-
#utilities
import copy
#modules
from smartPeak.core.smartPeak import smartPeak
from smartPeak.core.smartPeak_i import smartPeak_i
from smartPeak.core.smartPeak_openSWATH_py import smartPeak_openSWATH_py
from smartPeak.pyTOPP.MRMMapper import MRMMapper
from smartPeak.pyTOPP.OpenSwathChromatogramExtractor import OpenSwathChromatogramExtractor
from smartPeak.pyTOPP.OpenSwathRTNormalizer import OpenSwathRTNormalizer
from smartPeak.pyTOPP.OpenSwathFeatureXMLToTSV import OpenSwathFeatureXMLToTSV
from smartPeak.pyTOPP.MRMFeatureFilter import MRMFeatureFilter
from smartPeak.pyTOPP.MRMFeatureSelector import MRMFeatureSelector
from smartPeak.pyTOPP.MRMFeatureValidator import MRMFeatureValidator
from smartPeak.data.ReferenceDataMethods import ReferenceDataMethods
from . import data_dir
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

    def testOpenSWATH_py(
            self,
            filename_filenames = "BloodProject01_SWATH_filenames.csv",
            filename_params = "BloodProject01_MRMFeatureFinderScoring_params.csv",
            delimiter = ','
            ):
        """Run the openSWATH python pipeline
        
        Args:
            
        """
        filenames = data_dir + "/" + filename_filenames
        filename_params = data_dir + "/" + filename_params
        openSWATH_py = smartPeak_openSWATH_py()
        smartpeak_i = smartPeak_i()
        smartpeak_i.read_pythonParams(filename_filenames,delimiter)
        filenames = smartpeak_i.getData()
        smartpeak_i.clear_data()
        smartpeak_i.read_openMSParams(filename_params,delimiter)
        params = smartpeak_i.getData()
        smartpeak_i.clear_data()
        for filename in filenames:
            for sample,v in filename.items():
                print("processing sample "+ sample)
                # load in the files
                openSWATH_py.load_TraML(v)
                openSWATH_py.load_MSExperiment(v)
                openSWATH_py.load_Trafo(v,
                    params['MRMFeatureFinderScoring'])
                openSWATH_py.load_SWATHorDIA({})
                # run the openSWATH workflow for metabolomics
                openSWATH_py.openSWATH_py(
                    params['MRMFeatureFinderScoring'])
                openSWATH_py.filterAndSelect_py(
                    v,
                    params['MRMFeatureFilter.filter_MRMFeatures'],
                    params['MRMFeatureSelector.select_MRMFeatures_score'],
                    params['MRMFeatureSelector.schedule_MRMFeatures_qmip'])
                #TODO: assert()
                # store
                openSWATH_py.store_featureMap(v)
                # manual clear data for the next iteration
                openSWATH_py.clear_data()
        
    def test_validate_openSWATH(self,
        filename_filenames = "BloodProject01_SWATH_filenames.csv",
        filename_params = "BloodProject01_MRMFeatureFinderScoring_params.csv",
        delimiter=','):
        """Test openSWATH validation

        Args:

        """
        filenames = data_dir + "/" + filename_filenames
        filename_params = data_dir + "/" + filename_params
        openSWATH_py = smartPeak_openSWATH_py()

        smartpeak_i = smartPeak_i()
        smartpeak_i.read_pythonParams(filename_filenames,delimiter)
        filenames = smartpeak_i.getData()
        smartpeak_i.clear_data()
        smartpeak_i.read_openMSParams(filename_params,delimiter)
        params = smartpeak_i.getData()
        smartpeak_i.clear_data()
        for filename in filenames:
            for sample,v in filename.items():
                print("processing sample "+ sample)
                try:
                    # load in the validation data (if no data is found, continue to the next sample)
                    ReferenceDataMethods_params_I = []
                    ReferenceDataMethods_params_I.extend(params['ReferenceDataMethods.getAndProcess_referenceData_samples'])
                    sample_names_I = '''['%s']'''%(sample)
                    ReferenceDataMethods_params_I.append({'description': '', 'name': 'sample_names_I', 'type': 'list', 'value': sample_names_I})
                    openSWATH_py.load_validationData(
                        v,
                        ReferenceDataMethods_params_I
                        )
                    # load in the files
                    openSWATH_py.load_TraML(v)
                    openSWATH_py.load_SWATHorDIA({})
                    # validate the data
                    openSWATH_py.load_featureMap(v)
                    openSWATH_py.validate_py(params['MRMFeatureValidator.validate_MRMFeatures'])
                    #TODO: assert()
                    # # store
                    # openSWATH_py.store_featureMap(v)
                except Exception as e:
                    print(e)
                # manual clear data for the next iteration
                openSWATH_py.clear_data()