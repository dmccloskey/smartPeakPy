# -*- coding: utf-8 -*-
from .SequenceGroupProcessor import SequenceGroupProcessor


class SequenceProcessor():

    def loadResources(
        self, 
        sequence_handler_IO, sequence_group_handler_IO,
        session_id
    ):
        """Load all files for the given session
        """

    def processSequence(
        self, sequence_handler_IO,
        sample_names=[],
        sequence_group_names=[],
        raw_data_processing_methods={},
        sequence_group_processing_methods={}
    ):
        """process a sequence of samples
        
        Args:
            sequence_handler_IO (SequenceHandler): the sequence class
            sample_names (list): name of the sample
            sequence_group_names (list): name of the sequence group
            raw_data_process_methods (list): name of the raw data method to execute
            sequence_group_processing_methods (list): name of the sequence method to execute            
        """
        # classes
        seqGroupProcessor = SequenceGroupProcessor()
        seqHandler = SequenceHandler()
        seqWriter = SequenceWriter()
        seqReader = SequenceReader()
        rawDataProcessor = RawDataProcessor()
        fileReaderOpenMS = FileReaderOpenMS()
        fileWriterOpenMS = FileWriterOpenMS()
        fileReader = FileReader()

        # process by sequence group
        for sequence_group in sequence_handler_IO.sequence_groups:
            # 1: process all Standards
            sample_indices = seqGroupProcessor.getSampleIndicesBySampleType(
                sequenceGroupHandler_I=sequence_group,
                sequenceHandler_I=sequence_handler_IO,
                sample_type="Standard"
            )
            # process the raw data
            for index in sample_indices:
                self.processRawData(
                    sequence_handler_IO.sequence[index], raw_data_processing_methods)
            # calculate the calibration curves
            calibrators = []
            for index in sample_indices:
                if sequence_handler_IO.sequence[index].raw_data_processing == "calculate_calibration":
                    calibrators.append(sequence_handler_IO.sequence[index])  # where is the actual concentrations?

            # 2: process all Unknowns
            # 3: process all Blanks, Double Blanks, and Solvents

    def processRawData(self, raw_data_handler_IO, raw_data_processing_methods):
        """Execute all raw data processing on the raw data"""

        rawDataHandler = RawDataHandler()

