# -*- coding: utf-8 -*-
from .SequenceGroupProcessor import SequenceGroupProcessor
from .SequenceGroupHandler import SequenceGroupHandler
from .RawDataHandler import RawDataHandler
from .RawDataProcessor import RawDataProcessor
from smartPeak.io.SequenceReader import SequenceReader
from smartPeak.io.FileReaderOpenMS import FileReaderOpenMS
import copy


class SequenceProcessor():

    def createSequence(
        self,
        sequenceHandler_IO, 
        filenames={},
        delimiter=",",
        verbose_I=False
    ):
        """Create a new session from files or wizard
        
        Args:
            sequenceHandler_IO (SequenceHandler): sequence handler
            filenames (dict): map of filetype to filename
            delimiter (str): string delimiter of the imported text file
            verbose_I (boolean): verbosity
        """
        rawDataHandler = RawDataHandler()
        sequenceGroupHandler = SequenceGroupHandler()

        # load sequence assets
        if filenames:  # load sequence from disk files 
            # read in the sequence file
            seqReader = SequenceReader()
            seqReader.read_sequenceFile(
                sequenceHandler_IO, filenames["sequence_csv_i"], delimiter)
            # read in the parameters
            seqReader.read_sequenceParameters(
                sequenceHandler_IO, filenames["parameters_csv_i"], delimiter)

            # load rawDataHandler files (applies to the whole session)
            fileReaderOpenMS = FileReaderOpenMS()
            fileReaderOpenMS.load_TraML(
                rawDataHandler, filenames, verbose_I=verbose_I)
            fileReaderOpenMS.load_featureFilter(
                rawDataHandler, filenames, verbose_I=verbose_I)
            fileReaderOpenMS.load_featureQC(
                rawDataHandler, filenames, verbose_I=verbose_I)
            # raw data files (i.e., mzML will be loaded dynamically)

            # load sequenceGroupHandler files
            fileReaderOpenMS.load_quantitationMethods(
                sequenceGroupHandler, filenames, verbose_I=verbose_I)
            # fileReaderOpenMS.load_standardsConcentrations(
            #     sequenceGroupHandler, filenames, verbose_I=verbose_I)         
        else:  # load sequence from GUI
            pass
        
        # initialize the sequence
        self.groupSamplesInSequence(sequenceHandler_IO, sequenceGroupHandler)
        self.addRawDataHandlerToSequence(sequenceHandler_IO, rawDataHandler)

    def addRawDataHandlerToSequence(
        self, sequenceHandler_IO, rawDataHandler_I
    ):
        """Add template RawDataHandler and SequenceGroupHandler to all
        samples and sequence groups in the sequence
        
        Args:
            sequenceHandler_IO (SequenceHandler): sequence handler
            rawDataHandler_I (RawDataHandler): raw data handler
        """
        for sample in sequenceHandler_IO.sequence:
            # pass the same object that can be reused
            sample.raw_data = rawDataHandler_I

    def groupSamplesInSequence(self, sequenceHandler_IO, sequenceGroupHandler_I=None):
        """group samples in a sequence

        An optional template SequenceGroupHandler can be added to all groups
        
        Args:
            sequenceHandler_IO (SequenceHandler): sequence handler
            sequenceGroupHandler_I (SequenceGroupHandler): sequence group handler
        """

        sequence_groups_dict = {}
        for cnt, sample in enumerate(sequenceHandler_IO.sequence):
            if sample.meta_data["sequence_group_name"] not in sequence_groups_dict.keys():
                sequence_groups_dict[sample.meta_data["sequence_group_name"]] = []
            sequence_groups_dict[sample.meta_data["sequence_group_name"]].append(cnt)
        
        sequence_groups = []
        for k, v in sequence_groups_dict.items():
            # pass a copy that can be edited
            if sequenceGroupHandler_I is not None:
                sequenceGroupHandler = copy.copy(sequenceGroupHandler_I)
            else:
                sequenceGroupHandler = SequenceGroupHandler()
            sequenceGroupHandler.sequence_group_name = k
            sequenceGroupHandler.sample_indices = v
            sequence_groups.append(sequenceGroupHandler)

        sequenceHandler_IO.sequence_groups = sequence_groups

    def processSequenceGroups(
        self, sequenceHandler_IO,
        sample_names=[],
        sequence_group_names=[],
        raw_data_processing_methods={},
        sequence_group_processing_methods={},
        verbose_I=False
    ):
        """process a sequence of samples
        
        Args:
            sequenceHandler_IO (SequenceHandler): the sequence class
            sample_names (list): name of the sample
            sequence_group_names (list): name of the sequence group
            raw_data_process_methods (list): name of the raw data method to execute
            sequence_group_processing_methods (list): name of the sequence group
                method to execute
        """
        # classes
        seqGroupProcessor = SequenceGroupProcessor()
        rawDataProcessor = RawDataProcessor()

        # process by sequence group
        for sequence_group in sequenceHandler_IO.sequence_groups:
            # 1: process all Standards
            sample_indices = seqGroupProcessor.getSampleIndicesBySampleType(
                sequenceGroupHandler_I=sequence_group,
                sequenceHandler_I=sequenceHandler_IO,
                sample_type="Standard"
            )
            # pick, filter, select, and check
            raw_data_processing_methods = \
                sequenceHandler_IO.getDefaultRawDataProcessingWorkflow(None)
            for index in sample_indices:
                rawDataProcessor.processRawData(
                    sequenceHandler_IO.sequence[index].raw_data,
                    raw_data_processing_methods,
                    sequenceHandler_IO.parameters,
                    sequenceHandler_IO.sequence[index].meta_data["filename"])
            # calculate the calibration curves
            seqGroupProcessor.optimizeCalibrationCurves(
                sequence_group, sequenceHandler_IO)  # TODO: fix bug
            # quantify and check
            raw_data_processing_methods = {
                "pick_peaks": False,
                "filter_peaks": False,
                "select_peaks": False,
                "validate_peaks": False,
                "quantify_peaks": True,
                "check_peaks": True}
            for index in sample_indices:
                rawDataProcessor.processRawData(
                    sequenceHandler_IO.sequence[index].raw_data,
                    raw_data_processing_methods,
                    sequenceHandler_IO.parameters)
                # copy out the feature map
                sequenceHandler_IO.sequence[index].featureMap = \
                    sequenceHandler_IO.sequence[index].raw_data.featureMap

            # 2: process all Unknowns
            sample_indices = seqGroupProcessor.getSampleIndicesBySampleType(
                sequenceGroupHandler_I=sequence_group,
                sequenceHandler_I=sequenceHandler_IO,
                sample_type="Unknown"
            )
            for index in sample_indices:
                # copy over updated quantitation_methods
                sequenceHandler_IO.sequence[index].raw_data.quantitation_methods = \
                    sequence_group.quantitation_methods
                rawDataProcessor.processRawData(
                    sequenceHandler_IO.sequence[index].raw_data,
                    sequenceHandler_IO.sequence[index].raw_data_processing,
                    sequenceHandler_IO.parameters,
                    sequenceHandler_IO.sequence[index].meta_data["filename"])
                # copy out the feature map
                sequenceHandler_IO.sequence[index].featureMap = \
                    sequenceHandler_IO.sequence[index].raw_data.featureMap

            # 3: process all QCs
            sample_indices = seqGroupProcessor.getSampleIndicesBySampleType(
                sequenceGroupHandler_I=sequence_group,
                sequenceHandler_I=sequenceHandler_IO,
                sample_type="QC"
            )
            for index in sample_indices:
                # copy over updated quantitation_methods
                sequenceHandler_IO.sequence[index].raw_data.quantitation_methods = \
                    sequence_group.quantitation_methods
                rawDataProcessor.processRawData(
                    sequenceHandler_IO.sequence[index].raw_data,
                    sequenceHandler_IO.sequence[index].raw_data_processing,
                    sequenceHandler_IO.parameters,
                    sequenceHandler_IO.sequence[index].meta_data["filename"])
                # copy out the feature map
                sequenceHandler_IO.sequence[index].featureMap = \
                    sequenceHandler_IO.sequence[index].raw_data.featureMap
            # # calculate the QCs
            # seqGroupProcessor.calculateQCs(
            #     sequence_group, sequenceHandler_IO)

            # 4: process all Blanks
            sample_indices = seqGroupProcessor.getSampleIndicesBySampleType(
                sequenceGroupHandler_I=sequence_group,
                sequenceHandler_I=sequenceHandler_IO,
                sample_type="Blank"
            )
            for index in sample_indices:
                # copy over updated quantitation_methods
                sequenceHandler_IO.sequence[index].raw_data.quantitation_methods = \
                    sequence_group.quantitation_methods
                rawDataProcessor.processRawData(
                    sequenceHandler_IO.sequence[index].raw_data,
                    sequenceHandler_IO.sequence[index].raw_data_processing,
                    sequenceHandler_IO.parameters,
                    sequenceHandler_IO.sequence[index].meta_data["filename"])
                # copy out the feature map
                sequenceHandler_IO.sequence[index].featureMap = \
                    sequenceHandler_IO.sequence[index].raw_data.featureMap
            
            # 5: process all Double Blanks
            sample_indices = seqGroupProcessor.getSampleIndicesBySampleType(
                sequenceGroupHandler_I=sequence_group,
                sequenceHandler_I=sequenceHandler_IO,
                sample_type="Double Blank"
            )
            for index in sample_indices:
                rawDataProcessor.processRawData(
                    sequenceHandler_IO.sequence[index].raw_data,
                    sequenceHandler_IO.sequence[index].raw_data_processing,
                    sequenceHandler_IO.parameters,
                    sequenceHandler_IO.sequence[index].meta_data["filename"])

            # 6: process all Solvents
            sample_indices = seqGroupProcessor.getSampleIndicesBySampleType(
                sequenceGroupHandler_I=sequence_group,
                sequenceHandler_I=sequenceHandler_IO,
                sample_type="Solvent"
            )
            for index in sample_indices:
                rawDataProcessor.processRawData(
                    sequenceHandler_IO.sequence[index].raw_data,
                    sequenceHandler_IO.sequence[index].raw_data_processing,
                    sequenceHandler_IO.parameters,
                    sequenceHandler_IO.sequence[index].meta_data["filename"])
                # copy out the feature map
                sequenceHandler_IO.sequence[index].featureMap = \
                    sequenceHandler_IO.sequence[index].raw_data.featureMap
            # # calculate the carryover
            # seqGroupProcessor.calculateCarryover(
            #     sequence_group, sequenceHandler_IO)