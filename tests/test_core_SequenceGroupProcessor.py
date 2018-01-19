# -*- coding: utf-8 -*-
from smartPeak.core.SequenceGroupProcessor import SequenceGroupProcessor
from smartPeak.core.SequenceGroupHandler import SequenceGroupHandler
from smartPeak.core.SequenceHandler import SequenceHandler
import copy


class TestSequenceGroupProcessor():
    """tests for SequenceGroupProcessor class
    """

    def test_checkSequenceGroupProcessing(self):
        sequenceGroupProcessor = SequenceGroupProcessor()

        events = [
            "calculate_calibration",
            "calculate_carryover",
            "calculate_variability"]
        assert(sequenceGroupProcessor.checkSequenceGroupProcessing(events))
        
        events = [
            "calculate_calibration",
            "carryover",
            "calculate_variability"]
        assert(~sequenceGroupProcessor.checkSequenceGroupProcessing(events))

    def test_getDefaultSequenceGroupProcessingWorkflow(self):
        sequenceGroupProcessor = SequenceGroupProcessor()

        assert(sequenceGroupProcessor.getDefaultSequenceGroupProcessingWorkflow(
            "Unknown") == [])
        assert(sequenceGroupProcessor.getDefaultSequenceGroupProcessingWorkflow(
            "Standard") == ["calculate_calibration"])
        assert(sequenceGroupProcessor.getDefaultSequenceGroupProcessingWorkflow(
            "QC") == ["calculate_variability"])
        assert(sequenceGroupProcessor.getDefaultSequenceGroupProcessingWorkflow(
            "Blank") == [])
        assert(sequenceGroupProcessor.getDefaultSequenceGroupProcessingWorkflow(
            "Double Blank") == [])
        assert(sequenceGroupProcessor.getDefaultSequenceGroupProcessingWorkflow(
            "Solvent") == ["calculate_carryover"])

    def test_getSampleIndicesBySampleType(self):
        sequenceHandler = SequenceHandler()
        sequenceGroupHandler = SequenceGroupHandler()
        sequenceGroupProcessor = SequenceGroupProcessor()

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
            'sequence_group_name': 'sequence_group', 'sample_type': 'Standard'})
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
        sequenceGroupHandler.sample_indices = [0, 1, 2]

        sample_indices = sequenceGroupProcessor.getSampleIndicesBySampleType(
            sequenceGroupHandler,
            sequenceHandler,
            "Unknown"
        )
        assert(sample_indices == [0, 2])

    def test_optimizeCalibrationCurves(self):
        """No test"""
        # sequenceHandler = SequenceHandler()
        # sequenceGroupHandler = SequenceGroupHandler()
        # sequenceGroupProcessor = SequenceGroupProcessor()

        pass