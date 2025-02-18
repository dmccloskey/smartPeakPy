# -*- coding: utf-8 -*-
from smartPeak.core.SequenceHandler import SequenceHandler
import copy
# 3rd part libraries
try:
    import pyopenms
except ImportError as e:
    print(e)


class TestSequenceHandler():

    def test_addSampleToSequence(self):
        sequenceHandler = SequenceHandler()

        # test data
        meta_data_required = {h: None for h in sequenceHandler.getRequiredHeaders()}
        meta_data1 = copy.copy(meta_data_required)
        meta_data1.update({
            'filename': 'file1', 'sample_name': 'sample1', 'sample_group_name': 'sample',
            'sequence_segment_name': 'sequence_segment', 'sample_type': 'Unknown'})
        featuremap1 = None
        
        meta_data2 = copy.copy(meta_data_required)
        meta_data2.update({
            'filename': 'file2', 'sample_name': 'sample2', 'sample_group_name': 'sample',
            'sequence_segment_name': 'sequence_segment', 'sample_type': 'Unknown'})
        featuremap2 = None
        
        meta_data3 = copy.copy(meta_data_required)
        meta_data3.update({
            'filename': 'file3', 'sample_name': 'sample3', 'sample_group_name': 'sample',
            'sequence_segment_name': 'sequence_segment', 'sample_type': 'Unknown'})
        featuremap3 = None

        # add the injections to the sequence
        sequenceHandler.addSampleToSequence(meta_data1, featuremap1)
        sequenceHandler.addSampleToSequence(meta_data2, featuremap2)
        sequenceHandler.addSampleToSequence(meta_data3, featuremap3)

        assert(len(sequenceHandler.sequence) == 3)
        assert(sequenceHandler.index_to_sample[1] == 'sample2')
        assert(sequenceHandler.sample_to_index['sample2'] == 1)

    def test_getMetaValue(self):  
        sequenceHandler = SequenceHandler()

        # make the test data
        feature = pyopenms.Feature()
        feature.setRT(16.0)
        subordinate = pyopenms.Feature()
        subordinate.setMetaValue("calculated_concentration", 10.0)

        result = sequenceHandler.getMetaValue(feature, subordinate, "RT")
        assert(result == 16.0)
        result = sequenceHandler.getMetaValue(feature, subordinate, "calculated_concentration")
        assert(result == 10.0)

    def test_parse_metaData(self):  
        sequenceHandler = SequenceHandler()

        meta_data = {}
        try:
            sequenceHandler.parse_metaData(meta_data)
        except Exception as e:
            assert(isinstance(e, NameError))

        meta_data = {
            "sample_name": None, "sample_type": None,
            "sequence_segment_name": None, "sample_group_name": None,
            "comments": None, "acquisition_method": None, "processing_method": None,
            "rack_code": None, "plate_code": None, 
            "vial_position": None, "rack_position": None, 
            "plate_position": None,
            "injection_volume": None, "dilution_factor": None, 
            "weight_to_volume": None,
            "set_name": None, "filename": ""}
        try:
            sequenceHandler.parse_metaData(meta_data)
        except Exception as e:
            assert(isinstance(e, NameError))

        meta_data["sample_name"] = ""
        meta_data["sample_group_name"] = None
        meta_data["sequence_segment_name"] = ""
        meta_data["filename"] = ""
        meta_data["sample_type"] = ""
        try:
            sequenceHandler.parse_metaData(meta_data)
        except Exception as e:
            assert(isinstance(e, NameError))

        meta_data["sample_group_name"] = ""
        meta_data["sequence_segment_name"] = None
        try:
            sequenceHandler.parse_metaData(meta_data)
        except Exception as e:
            assert(isinstance(e, NameError))

        meta_data["sequence_segment_name"] = ""
        meta_data["filename"] = None
        try:
            sequenceHandler.parse_metaData(meta_data)
        except Exception as e:
            assert(isinstance(e, NameError))

        meta_data["filename"] = ""
        try:
            sequenceHandler.parse_metaData(meta_data)
        except Exception as e:
            assert(isinstance(e, NameError))

        meta_data["sample_type"] = "Unknown"
        assert(sequenceHandler.parse_metaData(meta_data)["sample_type"] == "Unknown")

    def test_getSamplesInSequence(self):
        sequenceHandler = SequenceHandler()

        # test data
        meta_data_required = {h: None for h in sequenceHandler.getRequiredHeaders()}
        meta_data1 = copy.copy(meta_data_required)
        meta_data1.update({
            'filename': 'file1', 'sample_name': 'sample1', 'sample_group_name': 'sample',
            'sequence_segment_name': 'sequence_segment', 'sample_type': 'Unknown'})
        featuremap1 = None
        
        meta_data2 = copy.copy(meta_data_required)
        meta_data2.update({
            'filename': 'file2', 'sample_name': 'sample2', 'sample_group_name': 'sample',
            'sequence_segment_name': 'sequence_segment', 'sample_type': 'Unknown'})
        featuremap2 = None
        
        meta_data3 = copy.copy(meta_data_required)
        meta_data3.update({
            'filename': 'file3', 'sample_name': 'sample3', 'sample_group_name': 'sample',
            'sequence_segment_name': 'sequence_segment', 'sample_type': 'Unknown'})
        featuremap3 = None

        # add the injections to the sequence
        sequenceHandler.addSampleToSequence(meta_data1, featuremap1)
        sequenceHandler.addSampleToSequence(meta_data2, featuremap2)
        sequenceHandler.addSampleToSequence(meta_data3, featuremap3)

        sample_names = ["sample1", "ample2", "sample3"]
        samples = sequenceHandler.getSamplesInSequence(sample_names)
        assert(samples[0].meta_data["sample_name"] == "sample1")
        assert(samples[1].meta_data["sample_name"] == "sample3")

    def test_parse_rawDataProcessing(self):
        sequenceHandler = SequenceHandler()
        # TODO

    def test_parse_sequenceSegmentProcessing(self):
        sequenceHandler = SequenceHandler()
        # TODO

    def test_getDefaultStaticFilenames(self):
        sequenceHandler = SequenceHandler()
        defaults = sequenceHandler.getDefaultStaticFilenames("Data")
        assert("sequence_csv_i" in defaults.keys())
        assert("parameters_csv_i" in defaults.keys())
        assert("traML_csv_i" in defaults.keys())
        assert("featureFilterComponents_csv_i" in defaults.keys())
        assert("featureFilterComponentGroups_csv_i" in defaults.keys())
        assert("featureQCComponents_csv_i" in defaults.keys())
        assert("featureQCComponentGroups_csv_i" in defaults.keys())
        assert("quantitationMethods_csv_i" in defaults.keys())
        assert("standardsConcentrations_csv_i" in defaults.keys())
        assert("db_json_i" in defaults.keys())

    def test_getDefaultDynamicFilenames(self):
        sequenceHandler = SequenceHandler()
        defaults = sequenceHandler.getDefaultDynamicFilenames("Data", "test1")
        assert("features_pdf_o" in defaults.keys())
        assert("calibrators_pdf_o" in defaults.keys())
        assert("mzML_i" in defaults.keys())
        assert("featureXML_o" in defaults.keys())
        assert("feature_csv_o" in defaults.keys())
        assert("featureXML_i" in defaults.keys())
        assert("quantitationMethods_csv_o" in defaults.keys())
        assert("componentsToConcentrations_csv_o" in defaults.keys())
