# -*- coding: utf-8 -*-
from smartPeak.core.SequenceSegmentProcessor import SequenceSegmentProcessor
from smartPeak.core.SequenceSegmentHandler import SequenceSegmentHandler
from smartPeak.core.SequenceHandler import SequenceHandler
import copy


class TestSequenceSegmentProcessor():
    """tests for SequenceSegmentProcessor class
    """

    def test_checkSequenceSegmentProcessing(self):
        sequenceSegmentProcessor = SequenceSegmentProcessor()

        events = [
            "calculate_calibration",
            "calculate_carryover",
            "calculate_variability"]
        assert(sequenceSegmentProcessor.checkSequenceSegmentProcessing(events))
        
        events = [
            "calculate_calibration",
            "carryover",
            "calculate_variability"]
        assert(~sequenceSegmentProcessor.checkSequenceSegmentProcessing(events))

    def test_getDefaultSequenceSegmentProcessingWorkflow(self):
        sequenceSegmentProcessor = SequenceSegmentProcessor()

        assert(sequenceSegmentProcessor.getDefaultSequenceSegmentProcessingWorkflow(
            "Unknown") == [])
        assert(sequenceSegmentProcessor.getDefaultSequenceSegmentProcessingWorkflow(
            "Standard") == ["calculate_calibration"])
        assert(sequenceSegmentProcessor.getDefaultSequenceSegmentProcessingWorkflow(
            "QC") == ["calculate_variability"])
        assert(sequenceSegmentProcessor.getDefaultSequenceSegmentProcessingWorkflow(
            "Blank") == [])
        assert(sequenceSegmentProcessor.getDefaultSequenceSegmentProcessingWorkflow(
            "Double Blank") == [])
        assert(sequenceSegmentProcessor.getDefaultSequenceSegmentProcessingWorkflow(
            "Solvent") == ["calculate_carryover"])

    def test_getSampleIndicesBySampleType(self):
        sequenceHandler = SequenceHandler()
        sequenceSegmentHandler = SequenceSegmentHandler()
        sequenceSegmentProcessor = SequenceSegmentProcessor()

        # test data
        meta_data_required = {h: None for h in sequenceHandler.getRequiredHeaders()}
        meta_data1 = copy.copy(meta_data_required)
        meta_data1.update({
            'filename': 'file1', 'sample_name': 'sample1', 'sample_group_name': 'sample',
            'sequence_segment_name': 'sequence_group', 'sample_type': 'Unknown'})
        featuremap1 = None
        
        meta_data2 = copy.copy(meta_data_required)
        meta_data2.update({
            'filename': 'file2', 'sample_name': 'sample2', 'sample_group_name': 'sample',
            'sequence_segment_name': 'sequence_group', 'sample_type': 'Standard'})
        featuremap2 = None
        
        meta_data3 = copy.copy(meta_data_required)
        meta_data3.update({
            'filename': 'file3', 'sample_name': 'sample3', 'sample_group_name': 'sample',
            'sequence_segment_name': 'sequence_group', 'sample_type': 'Unknown'})
        featuremap3 = None

        # add the injections to the sequence
        sequenceHandler.addSampleToSequence(meta_data1, featuremap1)
        sequenceHandler.addSampleToSequence(meta_data2, featuremap2)
        sequenceHandler.addSampleToSequence(meta_data3, featuremap3)
        sequenceSegmentHandler.sample_indices = [0, 1, 2]

        sample_indices = sequenceSegmentProcessor.getSampleIndicesBySampleType(
            sequenceSegmentHandler,
            sequenceHandler,
            "Unknown"
        )
        assert(sample_indices == [0, 2])

    def test_optimizeCalibrationCurves(self):
        sequenceHandler = SequenceHandler()
        sequenceSegmentHandler = SequenceSegmentHandler()
        sequenceSegmentProcessor = SequenceSegmentProcessor()

        # load in the test data

        # test
        sequenceSegmentProcessor.optimizeCalibrationCurves(
            sequenceSegmentHandler,
            sequenceHandler)
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            0].getComponentName() == "")
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            0].getISName() == "")
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            0].getFeatureName() == "")
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            0].getTransformationModelParams().getValue("slope") == 1.0)
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            0].getTransformationModelParams().getValue("intercept") == 1.0)
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            0].getNPoints() == 4)
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            0].getCorrelationCoefficient() == 0.99)
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            0].getLLOQ() == 0.99)
        assert(sequenceSegmentHandler.getQuantitationMethods()[
            0].getULOQ() == 0.99)

        pass