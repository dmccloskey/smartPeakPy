# -*- coding: utf-8 -*-
# modules
from smartPeak.io.FileReaderOpenMS import FileReaderOpenMS
from smartPeak.io.FileWriterOpenMS import FileWriterOpenMS
from smartPeak.core.RawDataHandler import RawDataHandler
from smartPeak.core.RawDataProcessor import RawDataProcessor
from . import data_dir


class TestRawDataProcessor():
    """tests for RawDataProcessor class
    """

    def load_data(self):
        filereader = FileReaderOpenMS()
        rawDataHandler = RawDataHandler()
        filename_params = '''%s%s''' % (data_dir, "params_1_core_RawDataProcessor.csv")
        filereader.read_rawDataProcessingParameters(rawDataHandler, filename_params, ",")
        self.params_1 = rawDataHandler.getParameters()
        rawDataHandler.clear()
        filename_params = '''%s%s''' % (data_dir, "params_2.csv")
        filereader.read_rawDataProcessingParameters(rawDataHandler, filename_params, ",")
        self.params_2 = rawDataHandler.getParameters()
        rawDataHandler.clear()

    def test_extract_metaData(self):
        self.load_data()
        rawDataHandler = RawDataHandler()
        rawDataProcessor = RawDataProcessor()
        fileReaderOpenMS = FileReaderOpenMS()
        
        # load traML
        traML_csv_i = '''%s%s''' % (data_dir, "traML_1.csv")
        fileReaderOpenMS.load_TraML(rawDataHandler, traML_csv_i)

        # load MSExperiment
        mzML_i = '''%s/mzML/%s''' % (data_dir, "mzML_1.mzML")
        fileReaderOpenMS.load_MSExperiment(rawDataHandler, mzML_i,
            MRMMapping_params_I=self.params_1['MRMMapping'])
        
        rawDataProcessor.extract_metaData(rawDataHandler)
        assert(
            rawDataHandler.meta_data['filename'] ==
            '''/home/user/code/tests/data//mzML/mzML_1.mzML''')
        assert(
            rawDataHandler.meta_data['sample_name'] ==
            '150601_0_BloodProject01_PLT_QC_Broth-1')

    def test_pickFeatures(self):
        self.load_data()
        rawDataHandler = RawDataHandler()
        rawDataProcessor = RawDataProcessor()
        fileReaderOpenMS = FileReaderOpenMS()
        fileWriterOpenMS = FileWriterOpenMS()
        
        # load traML
        traML_csv_i = '''%s%s''' % (data_dir, "traML_1.csv")
        fileReaderOpenMS.load_TraML(rawDataHandler, traML_csv_i)

        # load MSExperiment
        mzML_i = '''%s/mzML/%s''' % (data_dir, "mzML_1.mzML")
        fileReaderOpenMS.load_MSExperiment(
            rawDataHandler, mzML_i,
            MRMMapping_params_I=self.params_1['MRMMapping'])
        
        rawDataProcessor.extract_metaData(rawDataHandler)

        # load trafo
        # trafo_csv_i = '''%s%s''' % (data_dir, "trafo_1")
        fileReaderOpenMS.load_Trafo(
            rawDataHandler,
            None,
            self.params_1['MRMFeatureFinderScoring'])

        # load SWATH
        fileReaderOpenMS.load_SWATHorDIA(rawDataHandler, {})

        # run OpenSWATH
        rawDataProcessor.pickFeatures(
            rawDataHandler,
            self.params_1['MRMFeatureFinderScoring'])
        assert(rawDataHandler.featureMap[0].getSubordinates()[
            0].getMetaValue("peak_apex_int") == 266403.0)
        assert(rawDataHandler.featureMap[0].getSubordinates()[
            0].getMetaValue("native_id") == b'23dpg.23dpg_1.Heavy')
        assert(rawDataHandler.featureMap[0].getSubordinates()[
            0].getRT() == 953.665693772912)  # refactor to use pytest.approx
        assert(rawDataHandler.featureMap[50].getSubordinates()[
            0].getMetaValue("peak_apex_int") == 0.0)
        assert(rawDataHandler.featureMap[50].getSubordinates()[
            0].getMetaValue("native_id") == b'accoa.accoa_1.Heavy')
        assert(rawDataHandler.featureMap[50].getSubordinates()[
            0].getRT() == 1067.5447296543123)

        # store
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_1_core_RawDataProcessor") 
        feature_csv_o = '''%s/features/%s.csv''' % (data_dir, "test_1_core_RawDataProcessor")
        fileWriterOpenMS.store_featureMap(rawDataHandler, featureXML_o, feature_csv_o)

    def test_filterFeatures(self):
        self.load_data()
        rawDataHandler = RawDataHandler()
        rawDataProcessor = RawDataProcessor()
        fileReaderOpenMS = FileReaderOpenMS()
        fileWriterOpenMS = FileWriterOpenMS()
        
        # load traML
        traML_csv_i = '''%s%s''' % (data_dir, "traML_1.csv")
        fileReaderOpenMS.load_TraML(rawDataHandler, traML_csv_i)

        # load MSExperiment
        mzML_i = '''%s/mzML/%s''' % (data_dir, "mzML_1.mzML")
        fileReaderOpenMS.load_MSExperiment(
            rawDataHandler, mzML_i,
            MRMMapping_params_I=self.params_1['MRMMapping'])
        
        rawDataProcessor.extract_metaData(rawDataHandler)

        # load featureMap
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_1_core_RawDataProcessor") 
        fileReaderOpenMS.load_featureMap(rawDataHandler, featureXML_o)

        # filter and select
        featureFilterComponents_csv_i = '''%s%s''' % (
            data_dir, "mrmfeatureqccomponents_1.csv")
        featureFilterComponentGroups_csv_i = '''%s%s''' % (
            data_dir, "mrmfeatureqccomponentgroups_1.csv")
        fileReaderOpenMS.load_featureFilter(
            rawDataHandler, featureFilterComponents_csv_i,
            featureFilterComponentGroups_csv_i)
        rawDataProcessor.filterFeatures(
            rawDataHandler,
            self.params_1['MRMFeatureFilter.filter_MRMFeatures'])
        assert(rawDataHandler.featureMap[0].getSubordinates()[
            0].getMetaValue("peak_apex_int") == 266403.0)
        assert(rawDataHandler.featureMap[0].getSubordinates()[
            0].getMetaValue("native_id") == b'23dpg.23dpg_1.Heavy')
        assert(rawDataHandler.featureMap[0].getSubordinates()[
            0].getRT() == 953.665693772912)  # refactor to use pytest.approx
        assert(rawDataHandler.featureMap[50].getSubordinates()[
            0].getMetaValue("peak_apex_int") == 49333.0)
        assert(rawDataHandler.featureMap[50].getSubordinates()[
            0].getMetaValue("native_id") == b'arg-L.arg-L_1.Heavy')
        assert(rawDataHandler.featureMap[50].getSubordinates()[
            0].getRT() == 46.6521683373451)

        # store
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_2_core_RawDataProcessor") 
        feature_csv_o = '''%s/features/%s.csv''' % (data_dir, "test_2_core_RawDataProcessor")
        fileWriterOpenMS.store_featureMap(rawDataHandler, featureXML_o, feature_csv_o)

    def test_selectFeatures(self):
        self.load_data()
        rawDataHandler = RawDataHandler()
        rawDataProcessor = RawDataProcessor()
        fileReaderOpenMS = FileReaderOpenMS()
        fileWriterOpenMS = FileWriterOpenMS()
        
        # load traML
        traML_csv_i = '''%s%s''' % (data_dir, "traML_1.csv")
        fileReaderOpenMS.load_TraML(rawDataHandler, traML_csv_i)

        # load MSExperiment
        mzML_i = '''%s/mzML/%s''' % (data_dir, "mzML_1.mzML")
        fileReaderOpenMS.load_MSExperiment(
            rawDataHandler, mzML_i,
            MRMMapping_params_I=self.params_1['MRMMapping'])
        
        rawDataProcessor.extract_metaData(rawDataHandler)

        # load featureMap
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_2_core_RawDataProcessor") 
        fileReaderOpenMS.load_featureMap(rawDataHandler, featureXML_o)

        # select
        rawDataProcessor.selectFeatures(
            rawDataHandler,
            self.params_1['MRMFeatureSelector.select_MRMFeatures_qmip'],
            self.params_1['MRMFeatureSelector.schedule_MRMFeatures_qmip'])
        assert(rawDataHandler.featureMap[0].getSubordinates()[
            0].getMetaValue("peak_apex_int") == 266403.0)
        assert(rawDataHandler.featureMap[0].getSubordinates()[
            0].getMetaValue("native_id") == b'23dpg.23dpg_1.Heavy')
        assert(rawDataHandler.featureMap[0].getSubordinates()[
            0].getRT() == 953.665693772912)  # refactor to use pytest.approx
        assert(rawDataHandler.featureMap[50].getSubordinates()[
            0].getMetaValue("peak_apex_int") == 198161.0)
        assert(rawDataHandler.featureMap[50].getSubordinates()[
            0].getMetaValue("native_id") == b'glutacon.glutacon_1.Heavy')
        assert(rawDataHandler.featureMap[50].getSubordinates()[
            0].getRT() == 752.796003723621)

        # store
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_3_core_RawDataProcessor") 
        feature_csv_o = '''%s/features/%s.csv''' % (data_dir, "test_3_core_RawDataProcessor")
        fileWriterOpenMS.store_featureMap(rawDataHandler, featureXML_o, feature_csv_o)

    def test_validateFeatures(self):        
        self.load_data()
        rawDataHandler = RawDataHandler()
        rawDataProcessor = RawDataProcessor()
        fileReaderOpenMS = FileReaderOpenMS()

        # load featureMap
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_3_core_RawDataProcessor")
        fileReaderOpenMS.load_featureMap(rawDataHandler, featureXML_o)
        
        # load in the validation data 
        referenceData_csv_i = '''%s%s''' % (
            data_dir, "referenceData_1_core_RawDataProcessor.csv")
        ReferenceDataMethods_params_I = []
        ReferenceDataMethods_params_I.extend(self.params_1[
            'ReferenceDataMethods.getAndProcess_referenceData_samples'])
        sample_names_I = '''['%s']''' % ("150601_0_BloodProject01_PLT_QC_Broth-1")
        ReferenceDataMethods_params_I.append({
            'description': '', 'name': 'sample_names_I', 
            'type': 'list', 'value': sample_names_I})
        fileReaderOpenMS.load_validationData(
            rawDataHandler,
            referenceData_csv_i,
            ReferenceDataMethods_params_I
            )

        # validate the data
        rawDataProcessor.validateFeatures(
            rawDataHandler, self.params_1[
                'MRMFeatureValidator.validate_MRMFeatures'])
        assert(rawDataHandler.validation_metrics["accuracy"] == 0.98709677419354835)

    def test_quantifyComponents(self):
        rawDataHandler = RawDataHandler()
        rawDataProcessor = RawDataProcessor()
        fileReaderOpenMS = FileReaderOpenMS()
        
        # load the quantitation method
        quantitationMethods_csv_i = '''%s%s''' % (
            data_dir, "quantitationMethods_1.csv")
        fileReaderOpenMS.load_quantitationMethods(
            rawDataHandler,
            quantitationMethods_csv_i)

        # load featureMap
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_3_core_RawDataProcessor") 
        fileReaderOpenMS.load_featureMap(rawDataHandler, featureXML_o)

        # quantify the components
        rawDataProcessor.quantifyComponents(rawDataHandler)
        assert(rawDataHandler.featureMap[0].getSubordinates()[
                1].getMetaValue("native_id") == b'23dpg.23dpg_1.Light')
        assert(rawDataHandler.featureMap[0].getSubordinates()[
            1].getMetaValue("calculated_concentration") == 0.44335812456518986) 
        assert(rawDataHandler.featureMap[0].getSubordinates()[
            1].getMetaValue("concentration_units") == b'uM')

    def test_checkFeatures(self):
        self.load_data()
        rawDataHandler = RawDataHandler()
        rawDataProcessor = RawDataProcessor()
        fileReaderOpenMS = FileReaderOpenMS()
        
        # load traML
        traML_csv_i = '''%s%s''' % (data_dir, "traML_1.csv")
        fileReaderOpenMS.load_TraML(rawDataHandler, traML_csv_i)

        # load featureMap
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_3_core_RawDataProcessor") 
        fileReaderOpenMS.load_featureMap(rawDataHandler, featureXML_o)

        featureQCComponents_csv_i = '''%s%s''' % (
            data_dir, "mrmfeatureqccomponents_1.csv")
        featureQCComponentGroups_csv_i = '''%s%s''' % (
            data_dir, "mrmfeatureqccomponentgroups_1.csv")
        fileReaderOpenMS.load_featureQC(
            rawDataHandler, featureQCComponents_csv_i,
            featureQCComponentGroups_csv_i)
        rawDataProcessor.checkFeatures(
            rawDataHandler,
            self.params_1['MRMFeatureFilter.filter_MRMFeatures.qc'])

        assert(rawDataHandler.featureMap[0].getSubordinates()[
                1].getMetaValue("native_id") == b'23dpg.23dpg_1.Light')
        assert(rawDataHandler.featureMap[0].getSubordinates()[
            1].getMetaValue("QC_transition_pass")) 
        # assert(rawDataHandler.featureMap[0].getSubordinates()[
        #     1].getMetaValue("QC_transition_group_pass"))

    def test_getDefaultRawDataProcessingWorkflow(self):
        rawDataProcessor = RawDataProcessor()

        workflow = [
                "load_raw_data",
                "pick_features",
                "filter_features",
                "select_features",
                "quantify_features",
                "check_features"]
        assert(rawDataProcessor.getDefaultRawDataProcessingWorkflow(
            "Unknown") == workflow)
        assert(rawDataProcessor.getDefaultRawDataProcessingWorkflow(
            "Standard") == workflow)
        assert(rawDataProcessor.getDefaultRawDataProcessingWorkflow("QC") == workflow)
        assert(rawDataProcessor.getDefaultRawDataProcessingWorkflow("Blank") == workflow)
        workflow = [
                "load_raw_data",
                "pick_features",
                "filter_features",
                "select_features",
                "check_features"]
        assert(rawDataProcessor.getDefaultRawDataProcessingWorkflow(
            "Double Blank") == workflow)
        assert(rawDataProcessor.getDefaultRawDataProcessingWorkflow(
            "Solvent") == workflow)

    def test_checkRawDataProcessingWorkflow(self):
        rawDataProcessor = RawDataProcessor()

        raw_data_processing_methods = [
            "load_raw_data",
            "load_features",
            "pick_features",
            "filter_features",
            "select_features",
            "validate_features",
            "quantify_features",
            "check_features",
            "plot_features",
            "store_features",
            "clear_feature_history",
            "save_features",
            "annotate_used_features",
            ]
        assert(rawDataProcessor.checkRawDataProcessingWorkflow(
            raw_data_processing_methods))

        raw_data_processing_methods = ["load_features"]
        assert(~rawDataProcessor.checkRawDataProcessingWorkflow(
            raw_data_processing_methods))

    def test_processRawData(self):
        self.load_data()
        rawDataHandler = RawDataHandler()
        rawDataProcessor = RawDataProcessor()
        fileReaderOpenMS = FileReaderOpenMS()
        
        # load files
        traML_csv_i = '''%s%s''' % (data_dir, "traML_1.csv")
        fileReaderOpenMS.load_TraML(rawDataHandler, traML_csv_i)

        featureFilterComponents_csv_i = '''%s%s''' % (
            data_dir, "mrmfeatureqccomponents_1.csv")
        featureFilterComponentGroups_csv_i = '''%s%s''' % (
            data_dir, "mrmfeatureqccomponentgroups_1.csv")
        fileReaderOpenMS.load_featureFilter(
            rawDataHandler, featureFilterComponents_csv_i,
            featureFilterComponentGroups_csv_i)

        quantitationMethods_csv_i = '''%s%s''' % (
            data_dir, "quantitationMethods_1.csv")
        fileReaderOpenMS.load_quantitationMethods(
            rawDataHandler,
            quantitationMethods_csv_i)

        featureQCComponents_csv_i = '''%s%s''' % (
            data_dir, "mrmfeatureqccomponents_1.csv")
        featureQCComponentGroups_csv_i = '''%s%s''' % (
            data_dir, "mrmfeatureqccomponentgroups_1.csv")
        fileReaderOpenMS.load_featureQC(
            rawDataHandler, featureQCComponents_csv_i,
            featureQCComponentGroups_csv_i)

        # test all
        raw_data_processing_events = [
            "load_raw_data",
            "pick_features",
            "filter_features",
            "select_features",
            "quantify_features",
            "check_features"]

        mzML_i = '''%s/mzML/%s''' % (data_dir, "mzML_1.mzML")
        filenames = {'mzML_i': mzML_i}
        self.params_1.update(
            {'ChromatogramExtractor': []})

        for event in raw_data_processing_events:
            rawDataProcessor.processRawData(
                rawDataHandler, 
                event,
                parameters=self.params_1,
                filenames=filenames,
            )

        assert(rawDataHandler.featureMap[0].getSubordinates()[
            1].getMetaValue("QC_transition_pass")) 
        assert(rawDataHandler.featureMap[0].getSubordinates()[
            1].getMetaValue("calculated_concentration") == 0.44335812456518986) 
        assert(rawDataHandler.featureMap[0].getSubordinates()[
            1].getMetaValue("concentration_units") == b'uM')
        assert(rawDataHandler.featureMap[0].getSubordinates()[
            0].getMetaValue("peak_apex_int") == 266403.0)
        assert(rawDataHandler.featureMap[0].getSubordinates()[
            0].getMetaValue("native_id") == b'23dpg.23dpg_1.Heavy')
        assert(rawDataHandler.featureMap[0].getSubordinates()[
            0].getRT() == 953.665693772912)  # refactor to use pytest.approx
        assert(rawDataHandler.featureMap[49].getSubordinates()[
            0].getMetaValue("peak_apex_int") == 198161.0)
        assert(rawDataHandler.featureMap[49].getSubordinates()[
            0].getMetaValue("native_id") == b'glutacon.glutacon_1.Heavy')
        assert(rawDataHandler.featureMap[49].getSubordinates()[
            0].getRT() == 752.7960037236212)

    def test_annotateUsedFeatures(self):
        self.load_data()
        rawDataHandler = RawDataHandler()
        rawDataProcessor = RawDataProcessor()
        fileReaderOpenMS = FileReaderOpenMS()
        
        # load traML
        traML_csv_i = '''%s%s''' % (data_dir, "traML_1.csv")
        fileReaderOpenMS.load_TraML(rawDataHandler, traML_csv_i)

        # load MSExperiment
        mzML_i = '''%s/mzML/%s''' % (data_dir, "mzML_1.mzML")
        fileReaderOpenMS.load_MSExperiment(
            rawDataHandler, mzML_i,
            MRMMapping_params_I=self.params_1['MRMMapping'])
        
        rawDataProcessor.extract_metaData(rawDataHandler)

        # load featureMap
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_1_core_RawDataProcessor") 
        fileReaderOpenMS.load_featureMap(rawDataHandler, featureXML_o)
        rawDataProcessor.saveCurrentFeatureMapToHistory(rawDataHandler)
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_3_core_RawDataProcessor") 
        fileReaderOpenMS.load_featureMap(rawDataHandler, featureXML_o)

        # select
        rawDataProcessor.annotateUsedFeatures(
            rawDataHandler)
        assert(rawDataHandler.featureMap[0].getSubordinates()[
            0].getMetaValue("used_").decode("utf-8") == "true")
        assert(rawDataHandler.featureMap[0].getSubordinates()[
            0].getMetaValue("native_id") == b'23dpg.23dpg_1.Heavy')
        assert(rawDataHandler.featureMap[50].getSubordinates()[
            0].getMetaValue("used_").decode("utf-8") == "false")
        assert(rawDataHandler.featureMap[50].getSubordinates()[
            0].getMetaValue("native_id") == b'accoa.accoa_1.Heavy')

    def test_saveCurrentFeatureMapToHistory(self):
        self.load_data()
        rawDataHandler = RawDataHandler()
        rawDataProcessor = RawDataProcessor()
        fileReaderOpenMS = FileReaderOpenMS()
        
        # load traML
        traML_csv_i = '''%s%s''' % (data_dir, "traML_1.csv")
        fileReaderOpenMS.load_TraML(rawDataHandler, traML_csv_i)

        # load MSExperiment
        mzML_i = '''%s/mzML/%s''' % (data_dir, "mzML_1.mzML")
        fileReaderOpenMS.load_MSExperiment(
            rawDataHandler, mzML_i,
            MRMMapping_params_I=self.params_1['MRMMapping'])
        
        rawDataProcessor.extract_metaData(rawDataHandler)

        # load featureMap
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_1_core_RawDataProcessor") 
        fileReaderOpenMS.load_featureMap(rawDataHandler, featureXML_o)

        # save the features to history
        rawDataProcessor.saveCurrentFeatureMapToHistory(rawDataHandler)
        assert(rawDataHandler.getFeatureMapHistory()[-1][0].getSubordinates()[
            0].getMetaValue("peak_apex_int") == 266403.0)
        assert(rawDataHandler.getFeatureMapHistory()[-1][0].getSubordinates()[
            0].getMetaValue("native_id") == b'23dpg.23dpg_1.Heavy')
        assert(rawDataHandler.getFeatureMapHistory()[-1][0].getSubordinates()[
            0].getRT() == 953.665693772912)  # refactor to use pytest.approx
        assert(rawDataHandler.getFeatureMapHistory()[-1][50].getSubordinates()[
            0].getMetaValue("peak_apex_int") == 0.0)
        assert(rawDataHandler.getFeatureMapHistory()[-1][50].getSubordinates()[
            0].getMetaValue("native_id") == b'accoa.accoa_1.Heavy')
        assert(rawDataHandler.getFeatureMapHistory()[-1][50].getSubordinates()[
            0].getRT() == 1067.54472965431)
