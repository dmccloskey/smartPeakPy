# -*- coding: utf-8 -*-
#utilities
import copy
#modules
from smartPeak.core.smartPeak import smartPeak
from smartPeak.core.smartPeak_i import smartPeak_i
from smartPeak.core.smartPeak_o import smartPeak_o
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

class TestSmartPeakOpenSWATH_py():
    """tests for smartPeak_openSWATH_py
    """

    def test_openSWATH_py(
            self,
            filename_filenames = "BloodProject01_SWATH_filenames.csv",
            filename_params = "BloodProject01_MRMFeatureFinderScoring_params.csv",
            delimiter = ',',
            debug = True
            ):
        """Run the openSWATH python pipeline
        
        Args:
            
        """
        filename_filenames = data_dir + "/" + filename_filenames
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
                    mzML_i = '''%s/mzML/%s.mzML'''%(data_dir,sample)
                    traML_csv_i = '''%s/%s'''%(data_dir,v["traML_csv_i"])
                    trafo_csv_i = '''%s/%s'''%(data_dir,v["trafo_csv_i"])
                    featureXML_o = '''%s/features/%s.featureXML'''%(data_dir,sample) 
                    feature_csv_o = '''%s/features/%s.csv'''%(data_dir,sample)
                    # load in the files
                    openSWATH_py.load_TraML({'traML_csv_i':traML_csv_i})
                    openSWATH_py.load_SWATHorDIA({})
                    openSWATH_py.load_MSExperiment({'mzML_feature_i':mzML_i})
                    openSWATH_py.extract_metaData()
                    if debug:
                        assert(openSWATH_py.meta_data['filename'] == '/home/user/code/tests/data//mzML/150601_0_BloodProject01_PLT_QC_Broth-1.mzML')
                        assert(openSWATH_py.meta_data['samplename'] == '150601_0_BloodProject01_PLT_QC_Broth-1')
                    openSWATH_py.load_Trafo(
                        {},#{'trafo_csv_i':trafo_csv_i},
                        params['MRMFeatureFinderScoring'])
                    # run the openSWATH workflow for metabolomics
                    openSWATH_py.openSWATH_py(
                        params['MRMFeatureFinderScoring'])
                    if debug:
                        assert(openSWATH_py.featureMap[0].getSubordinates()[0].getMetaValue("peak_apex_int") == 262623.5)
                        assert(openSWATH_py.featureMap[0].getSubordinates()[0].getMetaValue("native_id") == b'23dpg.23dpg_1.Heavy')
                        assert(openSWATH_py.featureMap[0].getSubordinates()[0].getRT() == 15.894456338119507) #refactor to use pytest.approx
                        assert(openSWATH_py.featureMap[50].getSubordinates()[0].getMetaValue("peak_apex_int") == 1913.0)
                        assert(openSWATH_py.featureMap[50].getSubordinates()[0].getMetaValue("native_id") == b'6pgc.6pgc_1.Heavy')
                        assert(openSWATH_py.featureMap[50].getSubordinates()[0].getRT() == 13.66598913269043)
                    openSWATH_py.filterAndSelect_py(
                        {},
                        params['MRMFeatureFilter.filter_MRMFeatures'],
                        params['MRMFeatureSelector.select_MRMFeatures_qmip'],
                        params['MRMFeatureSelector.schedule_MRMFeatures_qmip'])
                    if debug:
                        assert(openSWATH_py.featureMap[0].getSubordinates()[0].getMetaValue("peak_apex_int") == 262623.5)
                        assert(openSWATH_py.featureMap[0].getSubordinates()[0].getMetaValue("native_id") == b'23dpg.23dpg_1.Heavy')
                        assert(openSWATH_py.featureMap[0].getSubordinates()[0].getRT() == 15.894456338119507) #refactor to use pytest.approx
                        assert(openSWATH_py.featureMap[50].getSubordinates()[0].getMetaValue("peak_apex_int") == 13919.000000000002)
                        assert(openSWATH_py.featureMap[50].getSubordinates()[0].getMetaValue("native_id") == b'glyclt.glyclt_1.Heavy')
                        assert(openSWATH_py.featureMap[50].getSubordinates()[0].getRT() == 3.1483763776143396) #refactor to use pytest.approx
                    else:
                        # store
                        openSWATH_py.store_featureMap(
                            {'featureXML_o':featureXML_o,
                            'feature_csv_o':feature_csv_o})
                except Exception as e:
                    print(e)
                    skipped_samples.append({'sample_name':sample,
                        'error_message':e})
                # manual clear data for the next iteration
                openSWATH_py.clear_data()
        if not debug:
            if skipped_samples:
                smartpeak_o = smartPeak_o(skipped_samples)
                skippedSamples_csv_i = '''%s/mzML/skippedSamples.csv'''%(data_dir)
                smartpeak_o.write_dict2csv(skippedSamples_csv_i)
        
    def test_validate_openSWATH(self,
        filename_filenames = "BloodProject01_SWATH_filenames.csv",
        filename_params = "BloodProject01_MRMFeatureFinderScoring_params.csv",
        db_ini_i = "/home/user/openMS_MRMworkflow/settings_metabolomics.ini",
        delimiter=',',
        debug = True):
        """Test openSWATH validation

        Args:

        """

        filename_filenames = data_dir + "/" + filename_filenames
        filename_params = data_dir + "/" + filename_params

        validation_metrics = []
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
                    # dynamically make the filenames
                    mzML_I = '''/mzML/%s.mzML'''%(sample)
                    referenceData_csv_i = '''%s/%s'''%(data_dir,v["referenceData_csv_i"])
                    # db_ini_i = '''%s/settings_metabolomics.ini'''%(data_dir)
                    featureXML_o = '''%s/features/%s.featureXML'''%(data_dir,sample) 
                    feature_csv_o = '''%s/features/%s.csv'''%(data_dir,sample)
                    # load in the validation data (if no data is found, continue to the next sample)
                    ReferenceDataMethods_params_I = []
                    ReferenceDataMethods_params_I.extend(params['ReferenceDataMethods.getAndProcess_referenceData_samples'])
                    sample_names_I = '''['%s']'''%(sample)
                    ReferenceDataMethods_params_I.append({'description': '', 'name': 'sample_names_I', 'type': 'list', 'value': sample_names_I})
                    openSWATH_py.load_validationData(
                        {'referenceData_csv_i':referenceData_csv_i},
                        # {'db_ini_i':db_ini_i},
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
                    if debug:
                        assert(openSWATH_py.validation_metrics["accuracy"] == 0.977941176471)
                    else:
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
        if not debug:
            if validation_metrics:
                smartpeak_o = smartPeak_o(validation_metrics)
                skippedSamples_csv_i = '''%s/mzML/skippedSamples.csv'''%(data_dir)
                smartpeak_o.write_dict2csv(validationMetrics_csv_i)
            if skipped_samples:
                smartpeak_o = smartPeak_o(skipped_samples)
                skippedSamples_csv_i = '''%s/mzML/skippedSamples.csv'''%(data_dir)
                smartpeak_o.write_dict2csv(skippedSamples_csv_i)