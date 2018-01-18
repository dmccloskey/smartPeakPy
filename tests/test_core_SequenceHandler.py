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
            'sequence_group_name': 'sequence_group', 'sample_type': 'Unknown'})
        featuremap1 = None
        
        meta_data2 = copy.copy(meta_data_required)
        meta_data2.update({
            'filename': 'file2', 'sample_name': 'sample2', 'sample_group_name': 'sample',
            'sequence_group_name': 'sequence_group', 'sample_type': 'Unknown'})
        featuremap2 = None
        
        meta_data3 = copy.copy(meta_data_required)
        meta_data3.update({
            'filename': 'file3', 'sample_name': 'sample3', 'sample_group_name': 'sample',
            'sequence_group_name': 'sequence_group', 'sample_type': 'Unknown'})
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
            "sequence_group_name": None, "sample_group_name": None,
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
        meta_data["sequence_group_name"] = ""
        meta_data["filename"] = ""
        meta_data["sample_type"] = ""
        try:
            sequenceHandler.parse_metaData(meta_data)
        except Exception as e:
            assert(isinstance(e, NameError))

        meta_data["sample_group_name"] = ""
        meta_data["sequence_group_name"] = None
        try:
            sequenceHandler.parse_metaData(meta_data)
        except Exception as e:
            assert(isinstance(e, NameError))

        meta_data["sequence_group_name"] = ""
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

    def test_addFeatureMapToSequence(self):
        sequenceHandler = SequenceHandler()

        # test data
        meta_data_required = {h: None for h in sequenceHandler.getRequiredHeaders()}
        meta_data1 = copy.copy(meta_data_required)
        meta_data1.update({
            'filename': 'file1', 'sample_name': 'sample1', 'sample_group_name': 'sample',
            'sequence_group_name': 'sequence_group', 'sample_type': 'Unknown'})
        featuremap1 = None
        
        meta_data2 = copy.copy(meta_data_required)
        meta_data2.update({
            'filename': 'file2', 'sample_name': 'sample2', 'sample_group_name': 'sample',
            'sequence_group_name': 'sequence_group', 'sample_type': 'Unknown'})
        featuremap2 = None
        
        meta_data3 = copy.copy(meta_data_required)
        meta_data3.update({
            'filename': 'file3', 'sample_name': 'sample3', 'sample_group_name': 'sample',
            'sequence_group_name': 'sequence_group', 'sample_type': 'Unknown'})
        featuremap3 = None

        # add the injections to the sequence
        sequenceHandler.addSampleToSequence(meta_data1, featuremap1)
        sequenceHandler.addSampleToSequence(meta_data2, featuremap2)
        sequenceHandler.addSampleToSequence(meta_data3, featuremap3)
        sequenceHandler.addFeatureMapToSequence("sample2", "DummyFeatureMap")

        assert(sequenceHandler.sequence[
            sequenceHandler.sample_to_index['sample2']].featureMap == "DummyFeatureMap")

    def test_getDefaultRawDataProcessingWorkflow(self):
        sequenceHandler = SequenceHandler()

        default = sequenceHandler.getDefaultRawDataProcessingWorkflow(None)
        assert(sequenceHandler.getDefaultRawDataProcessingWorkflow("Unknown") != default)
        assert(sequenceHandler.getDefaultRawDataProcessingWorkflow("Standard") != default)
        assert(sequenceHandler.getDefaultRawDataProcessingWorkflow("QC") != default)
        assert(sequenceHandler.getDefaultRawDataProcessingWorkflow("Blank") != default)
        assert(sequenceHandler.getDefaultRawDataProcessingWorkflow("Double Blank") == default)
        assert(sequenceHandler.getDefaultRawDataProcessingWorkflow("Solvent") == default)

    def test_getDefaultSequenceGroupProcessingWorkflow(self):
        sequenceHandler = SequenceHandler()

        default = sequenceHandler.getDefaultSequenceGroupProcessingWorkflow(None)
        assert(sequenceHandler.getDefaultSequenceGroupProcessingWorkflow("Unknown") == default)
        assert(sequenceHandler.getDefaultSequenceGroupProcessingWorkflow("Standard") != default)
        assert(sequenceHandler.getDefaultSequenceGroupProcessingWorkflow("QC") != default)
        assert(sequenceHandler.getDefaultSequenceGroupProcessingWorkflow("Blank") == default)
        assert(sequenceHandler.getDefaultSequenceGroupProcessingWorkflow("Double Blank") == default)
        assert(sequenceHandler.getDefaultSequenceGroupProcessingWorkflow("Solvent") != default)

    def test_parse_rawDataProcessing(self):
        sequenceHandler = SequenceHandler()
        # TODO

    def test_parse_sequenceGroupProcessing(self):
        sequenceHandler = SequenceHandler()
        # TODO
