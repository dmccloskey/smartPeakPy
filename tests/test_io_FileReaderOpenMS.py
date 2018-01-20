# -*- coding: utf-8 -*-
# modules
from smartPeak.io.FileReader import FileReader
from smartPeak.io.FileReaderOpenMS import FileReaderOpenMS
from smartPeak.core.RawDataHandler import RawDataHandler
from smartPeak.core.SequenceSegmentHandler import SequenceSegmentHandler
from . import data_dir
# 3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)


class TestFileReaderOpenMS():
    """tests for FileReaderOpenMS
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

    def test_load_traML(self):
        rawDataHandler = RawDataHandler()
        fileReaderOpenMS = FileReaderOpenMS()

        # load traML
        traML_csv_i = '''%s%s''' % (data_dir, "traML_1.csv")
        fileReaderOpenMS.load_TraML(rawDataHandler, traML_csv_i)
        assert(rawDataHandler.targeted.getTransitions()[0].getPeptideRef() == b'arg-L')
        assert(rawDataHandler.targeted.getTransitions()[0].getPrecursorMZ() == 179.0)
        assert(rawDataHandler.targeted.getTransitions()[0].getProductMZ() == 136.0)
        assert(rawDataHandler.targeted.getTransitions()[50].getPeptideRef() == b'ins')
        assert(rawDataHandler.targeted.getTransitions()[50].getPrecursorMZ() == 267.0)
        assert(rawDataHandler.targeted.getTransitions()[50].getProductMZ() == 108.0)

    def test_load_MSExperiment(self):
        self.load_data()
        rawDataHandler = RawDataHandler()
        fileReaderOpenMS = FileReaderOpenMS()
        
        # load traML
        traML_csv_i = '''%s%s''' % (data_dir, "traML_1.csv")
        fileReaderOpenMS.load_TraML(rawDataHandler, traML_csv_i)

        # load MSExperiment
        mzML_i = '''%s/mzML/%s''' % (data_dir, "mzML_1.mzML")
        fileReaderOpenMS.load_MSExperiment(rawDataHandler, mzML_i,
            MRMMapping_params_I=self.params_1['MRMMapping'])
        assert(rawDataHandler.msExperiment.getChromatograms()[
            0].getProduct().getMZ() == 0.0)
        assert(rawDataHandler.msExperiment.getChromatograms()[
            0].getPrecursor().getMZ() == 0.0)
        assert(rawDataHandler.msExperiment.getChromatograms()[
            0].getNativeID() == b'TIC')
        assert(rawDataHandler.chromatogram_map.getChromatograms()[
            0].getProduct().getMZ() == 136.0)
        assert(rawDataHandler.chromatogram_map.getChromatograms()[
            0].getPrecursor().getMZ() == 179.0)
        assert(rawDataHandler.chromatogram_map.getChromatograms()[
            0].getNativeID() == b'arg-L.arg-L_1.Heavy')

        # # Precursor chromatogramExtraction
        # # load traML
        # traML_csv_i = '''%s%s''' % (data_dir, "traML_2.csv")
        # fileReaderOpenMS.load_TraML(traML_csv_i)

        # # load MSExperiment
        # mzML_i = '''%s/mzML/%s''' % (data_dir, "mzML_2.mzML")
        # # chromatogramExtraction_params = {
        # #     "extract_window": 0.5,
        # #     "ppm": False,
        # #     "rt_extraction_window": -1,
        # #     "filter": "tophat",
        # #     "extract_precursors": True
        # # }
        # fileReaderOpenMS.load_MSExperiment(mzML_i,
        #     MRMMapping_params_I=self.params_2['MRMMapping'],
        #     chromatogramExtractor_params_I=self.params_2['ChromatogramExtractor'])
        # assert()
        # assert()

    def test_load_Trafo(self):
        self.load_data()
        rawDataHandler = RawDataHandler()
        fileReaderOpenMS = FileReaderOpenMS()
        
        # load traML
        traML_csv_i = '''%s%s''' % (data_dir, "traML_1.csv")
        fileReaderOpenMS.load_TraML(rawDataHandler, traML_csv_i)

        # load MSExperiment
        mzML_i = '''%s/mzML/%s''' % (data_dir, "mzML_1.mzML")
        fileReaderOpenMS.load_MSExperiment(
            rawDataHandler, mzML_i,
            MRMMapping_params_I=self.params_1['MRMMapping'])

        # load trafo
        fileReaderOpenMS.load_Trafo(
            rawDataHandler, 
            None,  # {'trafo_csv_i':trafo_csv_i},
            self.params_1['MRMFeatureFinderScoring'])
        assert(isinstance(rawDataHandler.trafo, pyopenms.TransformationDescription))

    def test_load_featureMap(self):
        rawDataHandler = RawDataHandler()
        fileReaderOpenMS = FileReaderOpenMS()

        # load featureMap
        featureXML_o = '''%s/features/%s.featureXML''' % (data_dir, "test_1") 
        fileReaderOpenMS.load_featureMap(rawDataHandler, featureXML_o)

        assert(rawDataHandler.featureMap[0].getSubordinates()[
            0].getMetaValue("peak_apex_int") == 266403.0)
        assert(rawDataHandler.featureMap[0].getSubordinates()[
            0].getMetaValue("native_id") == b'23dpg.23dpg_1.Heavy')
        assert(rawDataHandler.featureMap[0].getSubordinates()[
            0].getRT() == 15.8944563381195)  # refactor to use pytest.approx
        assert(rawDataHandler.featureMap[50].getSubordinates()[
            0].getMetaValue("peak_apex_int") == 0.0)
        assert(rawDataHandler.featureMap[50].getSubordinates()[
            0].getMetaValue("native_id") == b'acon-C.acon-C_1.Heavy')
        assert(rawDataHandler.featureMap[50].getSubordinates()[
            0].getRT() == 14.0348804560343)

    def test_load_quantitationMethods(self):
        sequenceSegmentHandler = SequenceSegmentHandler()
        fileReaderOpenMS = FileReaderOpenMS()

        # load the quantitation method
        quantitationMethods_csv_i = '''%s%s''' % (
            data_dir, "quantitationMethods_1.csv")
        fileReaderOpenMS.load_quantitationMethods(
            sequenceSegmentHandler, quantitationMethods_csv_i)
        assert(sequenceSegmentHandler.quantitation_methods[0].getLLOQ() == 0.25)
        assert(sequenceSegmentHandler.quantitation_methods[0].getULOQ() == 2.5)
        assert(sequenceSegmentHandler.quantitation_methods[
            0].getComponentName() == b'23dpg.23dpg_1.Light')

    def test_load_standardsConcentrations(self):
        sequenceSegmentHandler = SequenceSegmentHandler()
        fileReaderOpenMS = FileReaderOpenMS()

        # load the quantitation method
        standardsConcentrations_csv_i = '''%s%s''' % (
            data_dir, "standardsConcentrations_1.csv")
        fileReaderOpenMS.load_standardsConcentrations( 
            sequenceSegmentHandler, standardsConcentrations_csv_i)
        assert(sequenceSegmentHandler.standards_concentrations[0].getLLOQ() == 0.25)
        assert(sequenceSegmentHandler.standards_concentrations[0].getULOQ() == 2.5)
        assert(sequenceSegmentHandler.standards_concentrations[
            0].getComponentName() == b'23dpg.23dpg_1.Light')

    def test_load_featureFilter(self):
        rawDataHandler = RawDataHandler()
        fileReaderOpenMS = FileReaderOpenMS()

        # load traML
        featureFiltercsv_i = '''%s%s''' % (data_dir, "mrmfeatureqcs_1.csv")
        fileReaderOpenMS.load_featureFilter(rawDataHandler, featureFiltercsv_i)
        assert(rawDataHandler.feature_filter.component_qcs[
            0].component_name == b'arg-L.arg-L_1.Heavy')
        assert(rawDataHandler.feature_filter.component_group_qcs[
            0].component_group_name == b'arg-L')

    def test_load_featureQC(self):
        rawDataHandler = RawDataHandler()
        fileReaderOpenMS = FileReaderOpenMS()

        # load traML
        featureQC_csv_i = '''%s%s''' % (data_dir, "mrmfeatureqcs_1.csv")
        fileReaderOpenMS.load_featureQC(rawDataHandler, featureQC_csv_i)
        assert(rawDataHandler.feature_qc.component_qcs[
            0].component_name == b'arg-L.arg-L_1.Heavy')
        assert(rawDataHandler.feature_qc.component_group_qcs[
            0].component_group_name == b'arg-L')

    def test_read_rawDataProcessingParameters(self):
        """No test"""
        pass

    def test_parse_rawDataProcessingParameters(self):
        rawDataHandler = RawDataHandler()
        fileReaderOpenMS = FileReaderOpenMS()

        parameters_file = {'MRMFeatureFinderScoring': [{
                'name': 'stop_report_after_feature', 'value': '-1', 'type': 'int'}],
            'MRMTransitionGroupPicker': [{
                'name': 'stop_after_feature', 'value': '5', 'type': 'int'}],
            'MRMFeatureSelector.schedule_MRMFeatures_qmip': [{
                'name': 'nn_thresholds', 'value': '[4,4]', 'type': 'list'}],
            'MRMFeatureValidator.validate_MRMFeatures': [{
                'name': 'Tr_window', 'value': '0.05', 'type': 'float'}],
            'ReferenceDataMethods.getAndProcess_referenceData_samples': [{
                'name': 'experiment_ids_I', 'value': "['BloodProject01']",
                'type': 'list'}],
            'MRMFeatureSelector.select_MRMFeatures_score': [{
                'name': 'sn_ratio', 'value': 'lambda score: log(score)',
                'type': 'string'}],
            'MRMFeatureSelector.select_MRMFeatures_qmip': [{
                'name': 'var_log_sn_score', 'value': 'lambda score: 1/score',
                'type': 'string'}],
            # 'MRMMapping': [{
            #     'name': 'precursor_tolerance', 'value': '0.0009', 'type': 'float'}],
            'MRMFeatureFilter.filter_MRMFeatures': [{
                'name': 'flag_or_filter', 'value': 'filter', 'type': 'string'}],
            'MRMFeatureFilter.filter_MRMFeatures.qc': [{
                'name': 'flag_or_filter', 'value': 'flag', 'type': 'string'}],
            'FeaturePlotter': [{
                'name': 'export_format', 'value': 'pdf', 'type': 'string'}]}

        fileReaderOpenMS.parse_rawDataProcessingParameters(rawDataHandler, parameters_file)
        
        test_parameters = [ 
            "MRMFeatureFinderScoring",
            "MRMFeatureFilter.filter_MRMFeatures",
            "MRMFeatureSelector.select_MRMFeatures_qmip",
            "MRMFeatureSelector.schedule_MRMFeatures_qmip",
            "MRMFeatureSelector.select_MRMFeatures_score",
            "ReferenceDataMethods.getAndProcess_referenceData_samples",
            "MRMFeatureValidator.validate_MRMFeatures",
            "MRMFeatureFilter.filter_MRMFeatures.qc",
        ]
        assert("MRMMapping" in rawDataHandler.getParameters())
        assert(len(rawDataHandler.getParameters()["ChromatogramExtractor"]) == 0)
        for parameter in test_parameters:
            assert(len(rawDataHandler.getParameters()[parameter]) >= 1)

    