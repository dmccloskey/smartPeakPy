# -*- coding: utf-8 -*-
from smartPeak.core.RawDataHandler import RawDataHandler
from smartPeak.core.SequenceGroupHandler import SequenceGroupHandler
from smartPeak.core.SequenceProcessor import SequenceProcessor
from smartPeak.core.SequenceHandler import SequenceHandler
import copy


class TestSequenceProcessor():

    def test_groupSamplesInSequence(self):
        sequenceHandler = SequenceHandler()
        sequenceGroupHandler = SequenceGroupHandler()
        sequenceProcessor = SequenceProcessor()

        # test data
        meta_data_required = {h: None for h in sequenceHandler.getRequiredHeaders()}
        meta_data1 = copy.copy(meta_data_required)
        meta_data1.update({
            'filename': 'file1', 'sample_name': 'sample1', 'sample_group_name': 'sample',
            'sequence_group_name': 'sequence_group1', 'sample_type': 'Unknown'})
        featuremap1 = None
        
        meta_data2 = copy.copy(meta_data_required)
        meta_data2.update({
            'filename': 'file2', 'sample_name': 'sample2', 'sample_group_name': 'sample',
            'sequence_group_name': 'sequence_group1', 'sample_type': 'Standard'})
        featuremap2 = None
        
        meta_data3 = copy.copy(meta_data_required)
        meta_data3.update({
            'filename': 'file3', 'sample_name': 'sample3', 'sample_group_name': 'sample',
            'sequence_group_name': 'sequence_group2', 'sample_type': 'Unknown'})
        featuremap3 = None

        # add the injections to the sequence
        sequenceHandler.addSampleToSequence(meta_data1, featuremap1)
        sequenceHandler.addSampleToSequence(meta_data2, featuremap2)
        sequenceHandler.addSampleToSequence(meta_data3, featuremap3)
        
        sequenceGroupHandler.quantitation_methods = "Test"

        sequenceProcessor.groupSamplesInSequence(sequenceHandler, sequenceGroupHandler)
        assert(len(sequenceHandler.sequence_groups) == 2)
        assert(sequenceHandler.sequence_groups[0].sample_indices == [0, 1])
        assert(sequenceHandler.sequence_groups[1].sample_indices == [2])
        assert(sequenceHandler.sequence_groups[0].quantitation_methods == "Test")

    def test_addRawDataHandlerToSequence(self):
        sequenceHandler = SequenceHandler()
        sequenceProcessor = SequenceProcessor()
        rawDataHandler = RawDataHandler()

        # test data
        meta_data_required = {h: None for h in sequenceHandler.getRequiredHeaders()}
        meta_data1 = copy.copy(meta_data_required)
        meta_data1.update({
            'filename': 'file1', 'sample_name': 'sample1', 'sample_group_name': 'sample',
            'sequence_group_name': 'sequence_group1', 'sample_type': 'Unknown'})
        featuremap1 = None
        
        meta_data2 = copy.copy(meta_data_required)
        meta_data2.update({
            'filename': 'file2', 'sample_name': 'sample2', 'sample_group_name': 'sample',
            'sequence_group_name': 'sequence_group1', 'sample_type': 'Standard'})
        featuremap2 = None
        
        meta_data3 = copy.copy(meta_data_required)
        meta_data3.update({
            'filename': 'file3', 'sample_name': 'sample3', 'sample_group_name': 'sample',
            'sequence_group_name': 'sequence_group2', 'sample_type': 'Unknown'})
        featuremap3 = None

        # add the injections to the sequence
        sequenceHandler.addSampleToSequence(meta_data1, featuremap1)
        sequenceHandler.addSampleToSequence(meta_data2, featuremap2)
        sequenceHandler.addSampleToSequence(meta_data3, featuremap3)

        rawDataHandler.featureMap = "Test"

        sequenceProcessor.addRawDataHandlerToSequence(sequenceHandler, rawDataHandler)
        assert(sequenceHandler.sequence[0].raw_data.featureMap == "Test")
        assert(sequenceHandler.sequence[1].raw_data.featureMap == "Test")
        assert(sequenceHandler.sequence[2].raw_data.featureMap == "Test")