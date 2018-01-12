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
        seqhandler = SequenceHandler()

        # test data
        meta_data_required = {h: None for h in seqhandler.getRequiredHeaders()}
        meta_data1 = copy.copy(meta_data_required)
        meta_data1.update({
            'filename': 'file1', 'sample_name': 'sample1', 'sample_group_name': 'sample',
            'sample_type': 'Unknown'})
        featuremap1 = None
        
        meta_data2 = copy.copy(meta_data_required)
        meta_data2.update({
            'filename': 'file2', 'sample_name': 'sample2', 'sample_group_name': 'sample',
            'sample_type': 'Unknown'})
        featuremap2 = None
        
        meta_data3 = copy.copy(meta_data_required)
        meta_data3.update({
            'filename': 'file3', 'sample_name': 'sample3', 'sample_group_name': 'sample',
            'sample_type': 'Unknown'})
        featuremap3 = None

        # add the injections to the sequence
        seqhandler.addSampleToSequence(meta_data1, featuremap1)
        seqhandler.addSampleToSequence(meta_data2, featuremap2)
        seqhandler.addSampleToSequence(meta_data3, featuremap3)

        assert(len(seqhandler.sequence) == 3)
        assert(seqhandler.index_to_sample[1] == 'sample2')
        assert(seqhandler.sample_to_index['sample2'] == 1)

    def test_getMetaValue(self):  
        seqhandler = SequenceHandler()

        # make the test data
        feature = pyopenms.Feature()
        feature.setRT(16.0)
        subordinate = pyopenms.Feature()
        subordinate.setMetaValue("calculated_concentration", 10.0)

        result = seqhandler.getMetaValue(feature, subordinate, "RT")
        assert(result == 16.0)
        result = seqhandler.getMetaValue(feature, subordinate, "calculated_concentration")
        assert(result == 10.0)

    def test_parse_metaData(self):  
        seqhandler = SequenceHandler()

        meta_data = {}
        try:
            seqhandler.parse_metaData(meta_data)
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
            seqhandler.parse_metaData(meta_data)
        except Exception as e:
            assert(isinstance(e, NameError))

        meta_data["sample_name"] = ""
        meta_data["sample_group_name"] = None
        meta_data["sequence_group_name"] = ""
        meta_data["filename"] = ""
        meta_data["sample_type"] = ""
        try:
            seqhandler.parse_metaData(meta_data)
        except Exception as e:
            assert(isinstance(e, NameError))

        meta_data["sample_group_name"] = ""
        meta_data["sequence_group_name"] = None
        try:
            seqhandler.parse_metaData(meta_data)
        except Exception as e:
            assert(isinstance(e, NameError))

        meta_data["sequence_group_name"] = ""
        meta_data["filename"] = None
        try:
            seqhandler.parse_metaData(meta_data)
        except Exception as e:
            assert(isinstance(e, NameError))

        meta_data["filename"] = ""
        try:
            seqhandler.parse_metaData(meta_data)
        except Exception as e:
            assert(isinstance(e, NameError))

        meta_data["sample_type"] = "Unknown"
        assert(seqhandler.parse_metaData(meta_data)["sample_type"] == "Unknown")

    def test_addFeatureMapToSequence(self):
        seqhandler = SequenceHandler()

        # test data
        meta_data_required = {h: None for h in seqhandler.getRequiredHeaders()}
        meta_data1 = copy.copy(meta_data_required)
        meta_data1.update({
            'filename': 'file1', 'sample_name': 'sample1', 'sample_group_name': 'sample',
            'sample_type': 'Unknown'})
        featuremap1 = None
        
        meta_data2 = copy.copy(meta_data_required)
        meta_data2.update({
            'filename': 'file2', 'sample_name': 'sample2', 'sample_group_name': 'sample',
             'sample_type': 'Unknown'})
        featuremap2 = None
        
        meta_data3 = copy.copy(meta_data_required)
        meta_data3.update({
            'filename': 'file3', 'sample_name': 'sample3', 'sample_group_name': 'sample',
            'sample_type': 'Unknown'})
        featuremap3 = None

        # add the injections to the sequence
        seqhandler.addSampleToSequence(meta_data1, featuremap1)
        seqhandler.addSampleToSequence(meta_data2, featuremap2)
        seqhandler.addSampleToSequence(meta_data3, featuremap3)
        seqhandler.addFeatureMapToSequence("sample2", "DummyFeatureMap")

        injection = seqhandler.sequence[
            seqhandler.sample_to_index['sample2']]
        assert(injection["featureMap"] == "DummyFeatureMap")

    test_getDefaultSampleProcessingWorkflow():
        seqhandler = SequenceHandler()

        default = seqhandler.getDefaultSampleProcessingWorkflow(None)
        assert(seqhandler.getDefaultSampleProcessingWorkflow("Unknown") != default)
        assert(seqhandler.getDefaultSampleProcessingWorkflow("Standard") != default)
        assert(seqhandler.getDefaultSampleProcessingWorkflow("QC") != default)
        assert(seqhandler.getDefaultSampleProcessingWorkflow("Blank") != default)
        assert(seqhandler.getDefaultSampleProcessingWorkflow("Double Blank") == default)
        assert(seqhandler.getDefaultSampleProcessingWorkflow("Solvent") == default)

    test_getDefaultSequenceProcessingWorkflow():
        seqhandler = SequenceHandler()

        default = seqhandler.getDefaultSequenceProcessingWorkflow(None)
        assert(seqhandler.getDefaultSequenceProcessingWorkflow("Unknown") != default)
        assert(seqhandler.getDefaultSequenceProcessingWorkflow("Standard") != default)
        assert(seqhandler.getDefaultSequenceProcessingWorkflow("QC") != default)
        assert(seqhandler.getDefaultSequenceProcessingWorkflow("Blank") == default)
        assert(seqhandler.getDefaultSequenceProcessingWorkflow("Double Blank") == default)
        assert(seqhandler.getDefaultSequenceProcessingWorkflow("Solvent") != default)

    test_parse_sampleProcessing():
        seqhandler = SequenceHandler()
        # TODO

    test_parse_sequenceProcessing():
        seqhandler = SequenceHandler()
        # TODO
