# -*- coding: utf-8 -*-
from .SequenceSegmentProcessor import SequenceSegmentProcessor
from .SequenceSegmentHandler import SequenceSegmentHandler
from .RawDataHandler import RawDataHandler
from .RawDataProcessor import RawDataProcessor
from smartPeak.io.SequenceReader import SequenceReader
from smartPeak.io.FileReaderOpenMS import FileReaderOpenMS
import copy


class SequenceProcessor():

    def createSequence(
        self,
        sequenceHandler_IO, 
        delimiter=",",
        verbose_I=False
    ):
        """Create a new session from files or wizard
        
        Args:
            sequenceHandler_IO (SequenceHandler): sequence handler
            delimiter (str): string delimiter of the imported text file
            verbose_I (boolean): verbosity
        """
        rawDataHandler = RawDataHandler()
        sequenceSegmentHandler = SequenceSegmentHandler()

        # load sequence assets
        if sequenceHandler_IO.filenames is not None:  
            # load sequence from disk files

            # read in the sequence file
            seqReader = SequenceReader()
            seqReader.read_sequenceFile(
                sequenceHandler_IO, sequenceHandler_IO.filenames["sequence_csv_i"],
                delimiter)

            # load rawDataHandler files (applies to the whole session)
            fileReaderOpenMS = FileReaderOpenMS()
            fileReaderOpenMS.read_rawDataProcessingParameters(
                rawDataHandler, sequenceHandler_IO.filenames["parameters_csv_i"],
                delimiter)
            fileReaderOpenMS.load_TraML(
                rawDataHandler, sequenceHandler_IO.filenames["traML_csv_i"],
                verbose_I=verbose_I)
            fileReaderOpenMS.load_featureFilter(
                rawDataHandler, sequenceHandler_IO.filenames["featureFilter_csv_i"],
                verbose_I=verbose_I)
            fileReaderOpenMS.load_featureQC(
                rawDataHandler, sequenceHandler_IO.filenames["featureQC_csv_i"],
                verbose_I=verbose_I)
            # raw data files (i.e., mzML, trafo, etc.,  will be loaded dynamically)

            # load sequenceSegmentHandler files
            fileReaderOpenMS.load_quantitationMethods(
                sequenceSegmentHandler, sequenceHandler_IO.filenames[
                    "quantitationMethods_csv_i"],
                verbose_I=verbose_I)
            fileReaderOpenMS.load_standardsConcentrations(
                sequenceSegmentHandler, sequenceHandler_IO.filenames[
                    "standardsConcentrations_csv_i"],
                verbose_I=verbose_I)

            # copy over the quantitation_method to the rawDataHandler
            rawDataHandler.setQuantitationMethods(
                sequenceSegmentHandler.quantitation_methods)

        else:  # load sequence from GUI
            pass
        
        # initialize the sequence
        self.segmentSamplesInSequence(sequenceHandler_IO, sequenceSegmentHandler)
        self.addRawDataHandlerToSequence(sequenceHandler_IO, rawDataHandler)

    def addRawDataHandlerToSequence(
        self, sequenceHandler_IO, rawDataHandler_I
    ):
        """Add template RawDataHandler and SequenceSegmentHandler to all
        samples and sequence groups in the sequence
        
        Args:
            sequenceHandler_IO (SequenceHandler): sequence handler
            rawDataHandler_I (RawDataHandler): raw data handler
        """
        for sample in sequenceHandler_IO.sequence:
            # copy the object to persist the data
            sample.raw_data = copy.copy(rawDataHandler_I)

    def segmentSamplesInSequence(self, sequenceHandler_IO, sequenceSegmentHandler_I=None):
        """Segment samples in a sequence

        An optional template SequenceSegmentHandler can be added to all segments
        
        Args:
            sequenceHandler_IO (SequenceHandler): sequence handler
            sequenceSegmentHandler_I (SequenceSegmentHandler): sequence segment handler
        """

        sequence_segments_dict = {}
        for cnt, sample in enumerate(sequenceHandler_IO.sequence):
            if sample.meta_data["sequence_segment_name"] not in sequence_segments_dict.keys():
                sequence_segments_dict[sample.meta_data["sequence_segment_name"]] = []
            sequence_segments_dict[sample.meta_data["sequence_segment_name"]].append(cnt)
        
        sequence_segments = []
        for k, v in sequence_segments_dict.items():
            # pass a copy that can be edited
            if sequenceSegmentHandler_I is not None:
                sequenceSegmentHandler = copy.copy(sequenceSegmentHandler_I)
            else:
                sequenceSegmentHandler = SequenceSegmentHandler()
            sequenceSegmentHandler.sequence_segment_name = k
            sequenceSegmentHandler.sample_indices = v
            sequence_segments.append(sequenceSegmentHandler)

        sequenceHandler_IO.setSequenceSegments(sequence_segments)

    def groupSamplesInSequence(self, sequenceHandler_IO, sampleGroupHandler_I=None):
        """Group samples in a sequence

        An optional template SampleGroupHandler can be added to all groups
        
        Args:
            sequenceHandler_IO (SequenceHandler): sequence handler
            sampleGroupHandler_I (SampleGrouptHandler): sample group handler
        """
        pass

    def processSequence(
        self, sequenceHandler_IO,
        sample_names_I=[],
        raw_data_processing_methods_I={},
    ):
        """process a sequence of samples
        
        Args:
            sequenceHandler_IO (SequenceHandler): the sequence class
            sample_names_I (list): name of the sample
            raw_data_process_methods_I (list): name of the raw data method to execute
        """
        rawDataProcessor = RawDataProcessor()

        # handle user desired sample_names
        process_sequence = sequenceHandler_IO.sequence
        if sample_names_I:
            process_sequence = sequenceHandler_IO.getSamplesInSequence(sample_names_I)

        for sample in process_sequence:
            # handle user desired raw_data_processing_methods
            if raw_data_processing_methods_I:
                raw_data_processing_methods = raw_data_processing_methods_I
            else:
                raw_data_processing_methods = \
                    rawDataProcessor.getDefaultRawDataProcessingWorkflow(
                        sample.getMetaData()["sample_type"])
                # if sample.raw_data.quantitation_methods is None:
                #     raw_data_processing_methods["quantify_peak"] = False
                    
            # process the samples
            for event in raw_data_processing_methods:
                rawDataProcessor.processRawData(
                    sample.raw_data,
                    event,
                    sample.raw_data.parameters,
                    sequenceHandler_IO.getDefaultDynamicFilenames(
                        sequenceHandler_IO.getDirDynamic(),
                        sample.getMetaData()["sample_name"])
                    )

    def processSequenceSegments(
        self, sequenceHandler_IO,
        sequence_segment_names=[],
        sequence_segment_processing_methods_I=[],
        verbose_I=False
    ):
        """process a sequence of samples by sequence groups
        
        Args:
            sequenceHandler_IO (SequenceHandler): the sequence class
            sequence_segment_names (list): name of the sequence group
            sequence_segment_processing_methods_I (list): name of the sequence sequence
                method to execute
        """
        # classes
        sequenceSegmentProcessor = SequenceSegmentProcessor()

        # handle the user input
        sequence_segments = sequenceHandler_IO.getSequenceSegments()
        if sequence_segment_names:
            sequence_segments = [
                s for s in sequenceHandler_IO.getSequenceSegments() 
                if s in sequence_segment_names]

        # process by sequence segment
        for sequence_segment in sequence_segments:
            # handle user desired raw_data_processing_methods
            if sequence_segment_processing_methods_I:
                sequence_segment_processing_methods = \
                    sequence_segment_processing_methods_I
            else:
                sequence_segment_processing_methods_set = set()
                for sample_index in sequence_segment.getSampleIndices():
                    sample_type = sequenceHandler_IO.sequence[
                        sample_index].getMetaData()["sample_type"]
                    sequence_segment_processing_methods_set.update(
                        sequenceSegmentProcessor.getDefaultSequenceSegmentProcessingWorkflow(
                            sample_type))
                sequence_segment_processing_methods = list(
                    sequence_segment_processing_methods_set)
                    
            # process the sequence
            for event in sequence_segment_processing_methods:                
                sequenceSegmentProcessor.processSequenceSegment(
                    sequence_segment,
                    sequenceHandler_IO,
                    event,
                    sequenceHandler_IO.getSequence()[
                        sequence_segment.getSampleIndices()[
                            0]].getRawData().getParameters(),  # assumption
                    # that all parameters are the same for each sample in the
                    # sequence segment!
                    sequenceHandler_IO.getDefaultDynamicFilenames(
                        sequenceHandler_IO.getDirDynamic(),
                        sequence_segment.getSequenceSegmentName()))