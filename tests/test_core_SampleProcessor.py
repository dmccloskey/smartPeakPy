# -*- coding: utf-8 -*-
# modules
from smartPeak.io.FileReader import FileReader
from smartPeak.io.FileReaderOpenMS import FileReaderOpenMS
from smartPeak.core.SampleHandler import SampleHandler
from smartPeak.io.FileWriterOpenMS import FileWriterOpenMS
from smartPeak.core.SampleProcessor import SampleProcessor
from . import data_dir
# 3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)


class TestSampleProcessor():
    """tests for SampleProcessor class
    """

    def load_data(self):
        filereader = FileReader()
        filename_params = '''%s%s''' % (data_dir, "params_1.csv")
        filereader.read_openMSParams(filename_params, ",")
        self.params_1 = filereader.getData()
        filereader.clear_data()
        filename_params = '''%s%s''' % (data_dir, "params_2.csv")
        filereader.read_openMSParams(filename_params, ",")
        self.params_2 = filereader.getData()
        filereader.clear_data()

    def test_extract_metaData(self):
        self.load_data()
        sampleHandler = SampleHandler()
        sampleProcessor = SampleProcessor()
        fileReaderOpenMS = FileReaderOpenMS()
        
        # load traML
        traML_csv_i = '''%s%s''' % (data_dir, "traML_1.csv")
        fileReaderOpenMS.load_TraML(sampleHandler, {'traML_csv_i': traML_csv_i})

        # load MSExperiment
        mzML_i = '''%s/mzML/%s''' % (data_dir, "mzML_1.mzML")
        fileReaderOpenMS.load_MSExperiment(sampleHandler, {
            'mzML_feature_i': mzML_i},
            MRMMapping_params_I=self.params_1['MRMMapping'])
        
        sampleProcessor.extract_metaData(sampleHandler)
        assert(
            sampleHandler.meta_data['filename'] ==
            '''/home/user/code/tests/data//mzML/mzML_1.mzML''')
        assert(
            sampleHandler.meta_data['sample_name'] ==
            '150601_0_BloodProject01_PLT_QC_Broth-1')

    def test_openSWATH(self):
        self.load_data()
        sampleHandler = SampleHandler()
        sampleProcessor = SampleProcessor()
        fileReaderOpenMS = FileReaderOpenMS()
        fileWriterOpenMS = FileWriterOpenMS()
        
        # load traML
        traML_csv_i = '''%s%s''' % (data_dir, "traML_1.csv")
        fileReaderOpenMS.load_TraML(sampleHandler, {'traML_csv_i': traML_csv_i})

        # load MSExperiment
        mzML_i = '''%s/mzML/%s''' % (data_dir, "mzML_1.mzML")
        fileReaderOpenMS.load_MSExperiment(sampleHandler, {
            'mzML_feature_i': mzML_i},
            MRMMapping_params_I=self.params_1['MRMMapping'])
        
        sampleProcessor.extract_metaData(sampleHandler)

        # load trafo
        # trafo_csv_i = '''%s%s''' % (data_dir, "trafo_1")
        fileReaderOpenMS.load_Trafo(
            sampleHandler,
            {},  # {'trafo_csv_i':trafo_csv_i},
            self.params_1['MRMFeatureFinderScoring'])

        # load SWATH
        fileReaderOpenMS.load_SWATHorDIA(sampleHandler, {})

        # run OpenSWATH
        sampleProcessor.openSWATH(
            sampleHandler,
            self.params_1['MRMFeatureFinderScoring'])
        assert(sampleHandler.featureMap[0].getSubordinates()[
            0].getMetaValue("peak_apex_int") == 266403.0)
        assert(sampleHandler.featureMap[0].getSubordinates()[
            0].getMetaValue("native_id") == b'23dpg.23dpg_1.Heavy')
        assert(sampleHandler.featureMap[0].getSubordinates()[
            0].getRT() == 15.894456338119507)  # refactor to use pytest.approx
        assert(sampleHandler.featureMap[50].getSubordinates()[
            0].getMetaValue("peak_apex_int") == 0.0)
        assert(sampleHandler.featureMap[50].getSubordinates()[
            0].getMetaValue("native_id") == b'acon-C.acon-C_1.Heavy')
        assert(sampleHandler.featureMap[50].getSubordinates()[
            0].getRT() == 14.034880456034344)

        # store
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_1") 
        feature_csv_o = '''%s/features/%s.csv''' % (data_dir, "test_1")
        fileWriterOpenMS.store_featureMap(sampleHandler, {
            'featureXML_o': featureXML_o,
            'feature_csv_o': feature_csv_o})

    def test_filterAndSelect(self):
        self.load_data()
        sampleHandler = SampleHandler()
        sampleProcessor = SampleProcessor()
        fileReaderOpenMS = FileReaderOpenMS()
        fileWriterOpenMS = FileWriterOpenMS()
        
        # load traML
        traML_csv_i = '''%s%s''' % (data_dir, "traML_1.csv")
        fileReaderOpenMS.load_TraML(sampleHandler, {'traML_csv_i': traML_csv_i})

        # load MSExperiment
        mzML_i = '''%s/mzML/%s''' % (data_dir, "mzML_1.mzML")
        fileReaderOpenMS.load_MSExperiment(sampleHandler, {
            'mzML_feature_i': mzML_i},
            MRMMapping_params_I=self.params_1['MRMMapping'])
        
        sampleProcessor.extract_metaData(sampleHandler)

        # load featureMap
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_1") 
        fileReaderOpenMS.load_featureMap(sampleHandler, {'featureXML_i': featureXML_o})

        # filter and select
        mrmfeatureqcs_csv_i = '''%s%s''' % (data_dir, "mrmfeatureqcs_1.csv")
        sampleProcessor.filterAndSelect_py(
            sampleHandler,
            {'mrmfeatureqcs_csv_i': mrmfeatureqcs_csv_i},
            self.params_1['MRMFeatureFilter.filter_MRMFeatures'],
            self.params_1['MRMFeatureSelector.select_MRMFeatures_qmip'],
            self.params_1['MRMFeatureSelector.schedule_MRMFeatures_qmip'])
        assert(sampleHandler.featureMap[0].getSubordinates()[
            0].getMetaValue("peak_apex_int") == 266403.0)
        assert(sampleHandler.featureMap[0].getSubordinates()[
            0].getMetaValue("native_id") == b'23dpg.23dpg_1.Heavy')
        assert(sampleHandler.featureMap[0].getSubordinates()[
            0].getRT() == 15.8944563381195)  # refactor to use pytest.approx
        assert(sampleHandler.featureMap[50].getSubordinates()[
            0].getMetaValue("peak_apex_int") == 198161.0)
        assert(sampleHandler.featureMap[50].getSubordinates()[
            0].getMetaValue("native_id") == b'glutacon.glutacon_1.Heavy')
        assert(sampleHandler.featureMap[50].getSubordinates()[
            0].getRT() == 12.546641343689)

        # store
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_2") 
        feature_csv_o = '''%s/features/%s.csv''' % (data_dir, "test_2")
        fileWriterOpenMS.store_featureMap(sampleHandler, {
            'featureXML_o': featureXML_o,
            'feature_csv_o': feature_csv_o})

    def test_validate(self):        
        self.load_data()
        sampleHandler = SampleHandler()
        sampleProcessor = SampleProcessor()
        fileReaderOpenMS = FileReaderOpenMS()

        # load featureMap
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_2")
        fileReaderOpenMS.load_featureMap(sampleHandler, {'featureXML_i': featureXML_o})
        
        # load in the validation data 
        referenceData_csv_i = '''%s%s''' % (data_dir, "referenceData_1.csv")
        ReferenceDataMethods_params_I = []
        ReferenceDataMethods_params_I.extend(self.params_1[
            'ReferenceDataMethods.getAndProcess_referenceData_samples'])
        sample_names_I = '''['%s']''' % ("150601_0_BloodProject01_PLT_QC_Broth-1")
        ReferenceDataMethods_params_I.append({
            'description': '', 'name': 'sample_names_I', 
            'type': 'list', 'value': sample_names_I})
        fileReaderOpenMS.load_validationData(
            sampleHandler,
            {'referenceData_csv_i': referenceData_csv_i},
            ReferenceDataMethods_params_I
            )

        # validate the data
        sampleProcessor.validate(
            sampleHandler, self.params_1[
                'MRMFeatureValidator.validate_MRMFeatures'])
        assert(sampleHandler.validation_metrics["accuracy"] == 0.98709677419354835)

    def test_quantifyComponents(self):
        sampleHandler = SampleHandler()
        sampleProcessor = SampleProcessor()
        fileReaderOpenMS = FileReaderOpenMS()
        
        # load the quantitation method
        quantitationMethods_csv_i = '''%s%s''' % (
            data_dir, "quantitationMethods_1.csv")
        fileReaderOpenMS.load_quantitationMethods(
            sampleHandler,
            {'quantitationMethods_csv_i': quantitationMethods_csv_i})

        # load featureMap
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_2") 
        fileReaderOpenMS.load_featureMap(sampleHandler, {'featureXML_i': featureXML_o})

        # quantify the components
        sampleProcessor.quantifyComponents(sampleHandler)
        assert(sampleHandler.featureMap[0].getSubordinates()[
                1].getMetaValue("native_id") == b'23dpg.23dpg_1.Light')
        assert(sampleHandler.featureMap[0].getSubordinates()[
            1].getMetaValue("calculated_concentration") == 0.44335812456518986) 
        assert(sampleHandler.featureMap[0].getSubordinates()[
            1].getMetaValue("concentration_units") == b'uM')
