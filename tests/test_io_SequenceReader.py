# -*- coding: utf-8 -*-
from smartPeak.core.SequenceHandler import SequenceHandler
from smartPeak.io.SequenceReader import SequenceReader


class TestSequenceReader():

    def test_read_sequenceFile(self):
        """No test"""
        pass

    def test_parse_sequenceFile(self):
        """No test"""
        pass

    def test_read_sequenceParameters(self):
        """No test"""
        pass

    def test_parse_sequenceParameters(self):
        sequenceReader = SequenceReader()
        sequenceHandler_IO = SequenceHandler()

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

        sequenceReader.parse_sequenceParameters(sequenceHandler_IO, parameters_file)
        
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
        assert("MRMMapping" in sequenceHandler_IO.getParameters())
        assert(len(sequenceHandler_IO.getParameters()["ChromatogramExtractor"]) == 0)
        for parameter in test_parameters:
            assert(len(sequenceHandler_IO.getParameters()[parameter]) >= 1)