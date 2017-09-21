# -*- coding: utf-8 -*-
#utilities
import copy
#modules
from smartPeak.core.smartPeak import smartPeak
from smartPeak.core.smartPeak_i import smartPeak_i
from .smartPeak_o import smartPeak_o
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

    def test_openSWATH_py(
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

        skipped_samples = []

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
                    mzML_I = '''/home/user/mzML_validationData/%s.mzML'''%(sample)
                    traML_csv_i = '''%s/traML.csv'''%(data_dir)
                    trafo_csv_i = '''%s/trafo.csv'''%(data_dir)
                    db_ini_i = '''%s/settings_metabolomics.ini'''%(data_dir)
                    featureXML_o = '''%s/features/%s.featureXML'''%(data_dir,sample) 
                    feature_csv_o = '''%s/features/%s.csv'''%(data_dir,sample)
                    # load in the files
                    openSWATH_py.load_TraML({'traML_csv_i':traML_csv_i})
                    openSWATH_py.load_SWATHorDIA({})
                    openSWATH_py.load_MSExperiment({'mzML_feature_i':mzML_I})
                    openSWATH_py.load_Trafo(
                        {},#{'trafo_csv_i':trafo_csv_i},
                        params['MRMFeatureFinderScoring'])
                    # run the openSWATH workflow for metabolomics
                    openSWATH_py.openSWATH_py(
                        params['MRMFeatureFinderScoring'])
                    openSWATH_py.filterAndSelect_py(
                        {},
                        params['MRMFeatureFilter.filter_MRMFeatures'],
                        {},#params['MRMFeatureSelector.select_MRMFeatures_score'],
                        params['MRMFeatureSelector.schedule_MRMFeatures_qmip'])
                    # store
                    openSWATH_py.store_featureMap(
                        {'featureXML_o':featureXML_o,
                        'feature_csv_o':feature_csv_o})
                    #TODO: assert()
                except Exception as e:
                    print(e)
                    skipped_samples.append({'sample_name':sample,
                        'error_message':e})
                # manual clear data for the next iteration
                openSWATH_py.clear_data()
        if skipped_samples:
            smartpeak_o = smartPeak_o(skipped_samples)
            skippedSamples_csv_i = '''%s/mzML/skippedSamples.csv'''%(data_dir)
            smartpeak_o.write_dict2csv(skippedSamples_csv_i)
        
    def test_validate_openSWATH(self,
        filename_filenames = "BloodProject01_SWATH_filenames.csv",
        filename_params = "BloodProject01_validation_params.csv",
        delimiter=','):
        """Test openSWATH validation

        Args:

        """

        filenames = data_dir + "/" + filename_filenames
        filename_params = data_dir + "/" + filename_params

        validation_metrics = []
        skipped_samples = []
        from .smartPeak_openSWATH_py import smartPeak_openSWATH_py
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
                    # dynamically make the filenames
                    mzML_I = '''/mzML/%s.mzML'''%(sample)
                    db_ini_i = '''%s/settings_metabolomics.ini'''%(data_dir)
                    featureXML_o = '''%s/features/%s.featureXML'''%(data_dir,sample) 
                    feature_csv_o = '''%s/features/%s.csv'''%(data_dir,sample)
                    # load in the validation data (if no data is found, continue to the next sample)
                    ReferenceDataMethods_params_I = []
                    ReferenceDataMethods_params_I.extend(params['ReferenceDataMethods.getAndProcess_referenceData_samples'])
                    sample_names_I = '''['%s']'''%(sample)
                    ReferenceDataMethods_params_I.append({'description': '', 'name': 'sample_names_I', 'type': 'list', 'value': sample_names_I})
                    openSWATH_py.load_validationData(
                        {'db_ini_i':db_ini_i},
                        ReferenceDataMethods_params_I
                        )
                    if not openSWATH_py.reference_data:
                        skipped_samples.append({'sample_name':sample,
                            'error_message':'no reference data found'})
                        print('Reference data not found for sample ' + sample + '.')
                        continue
                    # validate the data
                    openSWATH_py.load_featureMap({'featureXML_i':featureXML_o})
                    openSWATH_py.validate_py(params['MRMFeatureValidator.validate_MRMFeatures'])
                    # store
                    openSWATH_py.store_featureMap(
                        {'featureXML_o':featureXML_o,
                        'feature_csv_o':feature_csv_o})
                    tmp = {}
                    tmp.update(openSWATH_py.validation_metrics)
                    tmp.update({'sample_name':sample})
                    validation_metrics.append(tmp)
                except Exception as e:
                    print(e)
                    skipped_samples.append({'sample_name':sample,
                        'error_message':e})
                # manual clear data for the next iteration
                openSWATH_py.clear_data()
        if skipped_samples:
            smartpeak_o = smartPeak_o(skipped_samples)
            skippedSamples_csv_i = '''%s/mzML/skippedSamples.csv'''%(data_dir)
            smartpeak_o.write_dict2csv(skippedSamples_csv_i)