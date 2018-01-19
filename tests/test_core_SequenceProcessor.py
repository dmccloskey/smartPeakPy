# -*- coding: utf-8 -*-
from smartPeak.core.RawDataHandler import RawDataHandler
from smartPeak.core.SequenceGroupHandler import SequenceGroupHandler
from smartPeak.core.SequenceProcessor import SequenceProcessor
from smartPeak.core.SequenceHandler import SequenceHandler
from . import data_dir
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

    def test_createSequence(self):
        sequenceHandler = SequenceHandler()
        sequenceProcessor = SequenceProcessor()

        filenames = {
            'sequence_csv_i': '''%s%s''' % (data_dir, "sequence_1.csv"),
            'parameters_csv_i': '''%s%s''' % (data_dir, "params_1.csv"),
            'traML_csv_i': '''%s%s''' % (data_dir, "traML_1.csv"),
            'featureFilter_csv_i': '''%s%s''' % (data_dir, "mrmfeatureqcs_1.csv"),
            'quantitationMethods_csv_i': '''%s%s''' % (
                data_dir, "quantitationMethods_1.csv"),
            'standardsConcentrations_csv_i': '''%s%s''' % (
                data_dir, "standardsConcentrations_1.csv"),
            'featureQC_csv_i': '''%s%s''' % (data_dir, "mrmfeatureqcs_1.csv"),
            }

        sequenceHandler.setFilenames(filenames)
        sequenceProcessor.createSequence(
            sequenceHandler, 
            delimiter=","
        )

        assert(sequenceHandler.sequence[0].meta_data[
            "sample_name"] == "170808_Jonathan_yeast_Sacc1_1x")
        assert(sequenceHandler.sequence[0].meta_data[
            "sample_group_name"] == "Test01")
        assert(sequenceHandler.sequence[
            0].raw_data.targeted.getTransitions()[
            0].getPeptideRef() == b'arg-L')
        assert(sequenceHandler.sequence[
            0].raw_data.feature_filter.component_qcs[
            0].component_name == b'arg-L.arg-L_1.Heavy')
        assert(sequenceHandler.sequence[
            0].raw_data.feature_qc.component_qcs[
            0].component_name == b'arg-L.arg-L_1.Heavy')
        assert(sequenceHandler.sequence[
            0].raw_data.quantitation_methods[
            0].getComponentName() == b'23dpg.23dpg_1.Light')
        assert(len(sequenceHandler.sequence_groups) == 1)
        assert(sequenceHandler.sequence_groups[
            0].quantitation_methods[
            0].getComponentName() == b'23dpg.23dpg_1.Light')

    def test_processSequence(self):
        sequenceHandler = SequenceHandler()
        sequenceProcessor = SequenceProcessor()

        filenames = {
            'sequence_csv_i': '''%s%s''' % (data_dir, "sequence_1.csv"),
            'parameters_csv_i': '''%s%s''' % (data_dir, "params_1.csv"),
            'traML_csv_i': '''%s%s''' % (data_dir, "traML_1.csv"),
            'featureFilter_csv_i': '''%s%s''' % (data_dir, "mrmfeatureqcs_1.csv"),
            'quantitationMethods_csv_i': '''%s%s''' % (
                data_dir, "quantitationMethods_1.csv"),
            'standardsConcentrations_csv_i': '''%s%s''' % (
                data_dir, "standardsConcentrations_1.csv"),
            'featureQC_csv_i': '''%s%s''' % (data_dir, "mrmfeatureqcs_1.csv"),
            }

        sequenceHandler.setFilenames(filenames)
        sequenceHandler.setDirDynamic(data_dir)
        raw_data_processing_methods = {
            "load_raw_data": True,
            "load_peaks": False,
            "pick_peaks": False,
            "filter_peaks": False,
            "select_peaks": False,
            "validate_peaks": False,
            "quantify_peaks": False,
            "check_peaks": False,
            "plot_peaks": False,
            "store_peaks": False}

        sequenceHandler.setFilenames(filenames)
        sequenceProcessor.createSequence(
            sequenceHandler,
            delimiter=","
        )
        sequenceProcessor.processSequence(
            sequenceHandler,
            raw_data_processing_methods_I=raw_data_processing_methods) 

        # TODO: add a formal test
        # for now, test should run without erroring out if all files are found 

    def test_processSequenceGroups(self):
        sequenceHandler = SequenceHandler()
        sequenceProcessor = SequenceProcessor()

        filenames = {
            'sequence_csv_i': '''%s%s''' % (data_dir, "sequence_1.csv"),
            'parameters_csv_i': '''%s%s''' % (data_dir, "params_1.csv"),
            'traML_csv_i': '''%s%s''' % (data_dir, "traML_1.csv"),
            'featureFilter_csv_i': '''%s%s''' % (data_dir, "mrmfeatureqcs_1.csv"),
            'quantitationMethods_csv_i': '''%s%s''' % (
                data_dir, "quantitationMethods_1.csv"),
            'standardsConcentrations_csv_i': '''%s%s''' % (
                data_dir, "standardsConcentrations_1.csv"),
            'featureQC_csv_i': '''%s%s''' % (data_dir, "mrmfeatureqcs_1.csv"),
            }

        sequenceHandler.setFilenames(filenames)
        sequenceProcessor.createSequence(
            sequenceHandler,
            delimiter=","
        )
        sequenceProcessor.processSequenceGroups(
            sequenceHandler)

        assert()