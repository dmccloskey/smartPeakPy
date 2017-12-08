# -*- coding: utf-8 -*-
# modules
from smartPeak.core.smartPeak_i import smartPeak_i
from smartPeak.core.smartPeak_o import smartPeak_o
from smartPeak.core.smartPeak_openSWATH_py import smartPeak_openSWATH_py
from . import data_dir
# 3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)


class TestSmartPeakOpenSWATH_py():
    """tests for smartPeak_openSWATH_py
    """

    def load_data(self):
        smartpeak_i = smartPeak_i()
        filename_params = '''%s%s''' % (data_dir, "params_1.csv")
        smartpeak_i.read_openMSParams(filename_params, ",")
        self.params_1 = smartpeak_i.getData()
        smartpeak_i.clear_data()
        filename_params = '''%s%s''' % (data_dir, "params_2.csv")
        smartpeak_i.read_openMSParams(filename_params, ",")
        self.params_2 = smartpeak_i.getData()
        smartpeak_i.clear_data()

    def test_load_traML(self):
        openSWATH_py = smartPeak_openSWATH_py()

        # load traML
        traML_csv_i = '''%s%s''' % (data_dir, "traML_1.csv")
        openSWATH_py.load_TraML({'traML_csv_i': traML_csv_i})
        assert(openSWATH_py.targeted.getTransitions()[0].getPeptideRef() == b'arg-L')
        assert(openSWATH_py.targeted.getTransitions()[0].getPrecursorMZ() == 179.0)
        assert(openSWATH_py.targeted.getTransitions()[0].getProductMZ() == 136.0)
        assert(openSWATH_py.targeted.getTransitions()[50].getPeptideRef() == b'ins')
        assert(openSWATH_py.targeted.getTransitions()[50].getPrecursorMZ() == 267.0)
        assert(openSWATH_py.targeted.getTransitions()[50].getProductMZ() == 108.0)

    def test_load_MSExperiment(self):
        self.load_data()
        openSWATH_py = smartPeak_openSWATH_py()
        
        # load traML
        traML_csv_i = '''%s%s''' % (data_dir, "traML_1.csv")
        openSWATH_py.load_TraML({'traML_csv_i': traML_csv_i})

        # load MSExperiment
        mzML_i = '''%s/mzML/%s''' % (data_dir, "mzML_1.mzML")
        openSWATH_py.load_MSExperiment({
            'mzML_feature_i': mzML_i},
            MRMMapping_params_I=self.params_1['MRMMapping'])
        assert(openSWATH_py.msExperiment.getChromatograms()[
            0].getProduct().getMZ() == 0.0)
        assert(openSWATH_py.msExperiment.getChromatograms()[
            0].getPrecursor().getMZ() == 0.0)
        assert(openSWATH_py.msExperiment.getChromatograms()[
            0].getNativeID() == b'TIC')
        assert(openSWATH_py.chromatogram_map.getChromatograms()[
            0].getProduct().getMZ() == 136.0)
        assert(openSWATH_py.chromatogram_map.getChromatograms()[
            0].getPrecursor().getMZ() == 179.0)
        assert(openSWATH_py.chromatogram_map.getChromatograms()[
            0].getNativeID() == b'arg-L.arg-L_1.Heavy')

        # # Precursor chromatogramExtraction
        # # load traML
        # traML_csv_i = '''%s%s''' % (data_dir, "traML_2.csv")
        # openSWATH_py.load_TraML({'traML_csv_i': traML_csv_i})

        # # load MSExperiment
        # mzML_i = '''%s/mzML/%s''' % (data_dir, "mzML_2.mzML")
        # # chromatogramExtraction_params = {
        # #     "extract_window": 0.5,
        # #     "ppm": False,
        # #     "rt_extraction_window": -1,
        # #     "filter": "tophat",
        # #     "extract_precursors": True
        # # }
        # openSWATH_py.load_MSExperiment({
        #     'mzML_feature_i': mzML_i},
        #     MRMMapping_params_I=self.params_2['MRMMapping'],
        #     chromatogramExtractor_params_I=self.params_2['ChromatogramExtractor'])
        # assert()
        # assert()

    def test_extract_metaData(self):
        self.load_data()
        openSWATH_py = smartPeak_openSWATH_py()
        
        # load traML
        traML_csv_i = '''%s%s''' % (data_dir, "traML_1.csv")
        openSWATH_py.load_TraML({'traML_csv_i': traML_csv_i})

        # load MSExperiment
        mzML_i = '''%s/mzML/%s''' % (data_dir, "mzML_1.mzML")
        openSWATH_py.load_MSExperiment({
            'mzML_feature_i': mzML_i},
            MRMMapping_params_I=self.params_1['MRMMapping'])
        
        openSWATH_py.extract_metaData()
        assert(
            openSWATH_py.meta_data['filename'] ==
            '''/home/user/code/tests/data//mzML/mzML_1.mzML''')
        assert(
            openSWATH_py.meta_data['sample_name'] ==
            '150601_0_BloodProject01_PLT_QC_Broth-1')

    def test_load_Trafo(self):
        self.load_data()
        openSWATH_py = smartPeak_openSWATH_py()
        
        # load traML
        traML_csv_i = '''%s%s''' % (data_dir, "traML_1.csv")
        openSWATH_py.load_TraML({'traML_csv_i': traML_csv_i})

        # load MSExperiment
        mzML_i = '''%s/mzML/%s''' % (data_dir, "mzML_1.mzML")
        openSWATH_py.load_MSExperiment({
            'mzML_feature_i': mzML_i},
            MRMMapping_params_I=self.params_1['MRMMapping'])
        
        openSWATH_py.extract_metaData()

        # load trafo
        openSWATH_py.load_Trafo(
            {},  # {'trafo_csv_i':trafo_csv_i},
            self.params_1['MRMFeatureFinderScoring'])
        assert(isinstance(openSWATH_py.trafo, pyopenms.TransformationDescription))

    def test_openSWATH_py(self):
        self.load_data()
        openSWATH_py = smartPeak_openSWATH_py()
        
        # load traML
        traML_csv_i = '''%s%s''' % (data_dir, "traML_1.csv")
        openSWATH_py.load_TraML({'traML_csv_i': traML_csv_i})

        # load MSExperiment
        mzML_i = '''%s/mzML/%s''' % (data_dir, "mzML_1.mzML")
        openSWATH_py.load_MSExperiment({
            'mzML_feature_i': mzML_i},
            MRMMapping_params_I=self.params_1['MRMMapping'])
        
        openSWATH_py.extract_metaData()

        # load trafo
        # trafo_csv_i = '''%s%s''' % (data_dir, "trafo_1")
        openSWATH_py.load_Trafo(
            {},  # {'trafo_csv_i':trafo_csv_i},
            self.params_1['MRMFeatureFinderScoring'])

        # load SWATH
        openSWATH_py.load_SWATHorDIA({})

        # run OpenSWATH
        openSWATH_py.openSWATH_py(
            self.params_1['MRMFeatureFinderScoring'])
        assert(openSWATH_py.featureMap[0].getSubordinates()[
            0].getMetaValue("peak_apex_int") == 262623.5)
        assert(openSWATH_py.featureMap[0].getSubordinates()[
            0].getMetaValue("native_id") == b'23dpg.23dpg_1.Heavy')
        assert(openSWATH_py.featureMap[0].getSubordinates()[
            0].getRT() == 15.894456338119507)  # refactor to use pytest.approx
        assert(openSWATH_py.featureMap[50].getSubordinates()[
            0].getMetaValue("peak_apex_int") == 50.5)
        assert(openSWATH_py.featureMap[50].getSubordinates()[
            0].getMetaValue("native_id") == b'actp.actp_1.Heavy')
        assert(openSWATH_py.featureMap[50].getSubordinates()[
            0].getRT() == 12.430290568542478)

        # store
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_1") 
        feature_csv_o = '''%s/features/%s.csv''' % (data_dir, "test_1")
        openSWATH_py.store_featureMap({
            'featureXML_o': featureXML_o,
            'feature_csv_o': feature_csv_o})

    def test_load_featureMap(self):
        openSWATH_py = smartPeak_openSWATH_py()
        
        # load traML
        traML_csv_i = '''%s%s''' % (data_dir, "traML_1.csv")
        openSWATH_py.load_TraML({'traML_csv_i': traML_csv_i})

        # load MSExperiment
        mzML_i = '''%s/mzML/%s''' % (data_dir, "mzML_1.mzML")
        openSWATH_py.load_MSExperiment({
            'mzML_feature_i': mzML_i},
            MRMMapping_params_I=self.params_1['MRMMapping'])
        
        openSWATH_py.extract_metaData()

        # load featureMap
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_1") 
        openSWATH_py.load_featureMap({'featureXML_i': featureXML_o})

        assert(openSWATH_py.featureMap[0].getSubordinates()[
            0].getMetaValue("peak_apex_int") == 262623.5)
        assert(openSWATH_py.featureMap[0].getSubordinates()[
            0].getMetaValue("native_id") == b'23dpg.23dpg_1.Heavy')
        assert(openSWATH_py.featureMap[0].getSubordinates()[
            0].getRT() == 15.8944563381195)  # refactor to use pytest.approx
        assert(openSWATH_py.featureMap[50].getSubordinates()[
            0].getMetaValue("peak_apex_int") == 50.5)
        assert(openSWATH_py.featureMap[50].getSubordinates()[
            0].getMetaValue("native_id") == b'actp.actp_1.Heavy')
        assert(openSWATH_py.featureMap[50].getSubordinates()[
            0].getRT() == 12.4302905685425)

    def test_filterAndSelect(self):
        self.load_data()
        openSWATH_py = smartPeak_openSWATH_py()
        
        # load traML
        traML_csv_i = '''%s%s''' % (data_dir, "traML_1.csv")
        openSWATH_py.load_TraML({'traML_csv_i': traML_csv_i})

        # load MSExperiment
        mzML_i = '''%s/mzML/%s''' % (data_dir, "mzML_1.mzML")
        openSWATH_py.load_MSExperiment({
            'mzML_feature_i': mzML_i},
            MRMMapping_params_I=self.params_1['MRMMapping'])
        
        openSWATH_py.extract_metaData()

        # load featureMap
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_1") 
        openSWATH_py.load_featureMap({'featureXML_i': featureXML_o})

        # filter and select
        mrmfeatureqcs_csv_i = '''%s%s''' % (data_dir, "mrmfeatureqcs_1.csv")
        openSWATH_py.filterAndSelect_py(
            {'mrmfeatureqcs_csv_i': mrmfeatureqcs_csv_i},
            self.params_1['MRMFeatureFilter.filter_MRMFeatures'],
            self.params_1['MRMFeatureSelector.select_MRMFeatures_qmip'],
            self.params_1['MRMFeatureSelector.schedule_MRMFeatures_qmip'])
        assert(openSWATH_py.featureMap[0].getSubordinates()[
            0].getMetaValue("peak_apex_int") == 262623.5)
        assert(openSWATH_py.featureMap[0].getSubordinates()[
            0].getMetaValue("native_id") == b'23dpg.23dpg_1.Heavy')
        assert(openSWATH_py.featureMap[0].getSubordinates()[
            0].getRT() == 15.8944563381195)  # refactor to use pytest.approx
        assert(openSWATH_py.featureMap[50].getSubordinates()[
            0].getMetaValue("peak_apex_int") == 92638.0)
        assert(openSWATH_py.featureMap[50].getSubordinates()[
            0].getMetaValue("native_id") == b'thr-L.thr-L_1.Heavy')
        assert(openSWATH_py.featureMap[50].getSubordinates()[
            0].getRT() == 1.0136314956665)
        # assert(openSWATH_py.featureMap[50].getSubordinates()[
        #     0].getMetaValue("peak_apex_int") == 1080.0)
        # assert(openSWATH_py.featureMap[50].getSubordinates()[
        #     0].getMetaValue("native_id") == b'oxa.oxa_1.Heavy')
        # assert(openSWATH_py.featureMap[50].getSubordinates()[
        #     0].getRT() == 13.4963475631714)

        # store
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_2") 
        feature_csv_o = '''%s/features/%s.csv''' % (data_dir, "test_2")
        openSWATH_py.store_featureMap({
            'featureXML_o': featureXML_o,
            'feature_csv_o': feature_csv_o})

    def test_validate_py(self):        
        self.load_data()
        openSWATH_py = smartPeak_openSWATH_py()

        # load featureMap
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_2")
        openSWATH_py.load_featureMap({'featureXML_i': featureXML_o})
        
        # load in the validation data 
        referenceData_csv_i = '''%s%s''' % (data_dir, "referenceData_1.csv")
        ReferenceDataMethods_params_I = []
        ReferenceDataMethods_params_I.extend(self.params_1[
            'ReferenceDataMethods.getAndProcess_referenceData_samples'])
        sample_names_I = '''['%s']''' % ("150601_0_BloodProject01_PLT_QC_Broth-1")
        ReferenceDataMethods_params_I.append({
            'description': '', 'name': 'sample_names_I', 
            'type': 'list', 'value': sample_names_I})
        openSWATH_py.load_validationData(
            {'referenceData_csv_i': referenceData_csv_i},
            ReferenceDataMethods_params_I
            )

        # validate the data
        openSWATH_py.validate_py(self.params_1[
            'MRMFeatureValidator.validate_MRMFeatures'])
        assert(openSWATH_py.validation_metrics["accuracy"] == 0.977941176471)