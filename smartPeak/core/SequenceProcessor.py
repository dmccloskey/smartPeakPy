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
            # read in the parameters
            seqReader.read_sequenceParameters(
                sequenceHandler_IO, sequenceHandler_IO.filenames["parameters_csv_i"],
                delimiter)

            # load rawDataHandler files (applies to the whole session)
            fileReaderOpenMS = FileReaderOpenMS()
            fileReaderOpenMS.load_TraML(
                rawDataHandler, sequenceHandler_IO.filenames["traML_csv_i"],
                verbose_I=verbose_I)
            fileReaderOpenMS.load_featureFilter(
                rawDataHandler, sequenceHandler_IO.filenames["featureFilter_csv_i"],
                verbose_I=verbose_I)
            fileReaderOpenMS.load_featureQC(
                rawDataHandler, sequenceHandler_IO.filenames["featureQC_csv_i"],
                verbose_I=verbose_I)
            fileReaderOpenMS.load_quantitationMethods(
                rawDataHandler, sequenceHandler_IO.filenames[
                    "quantitationMethods_csv_i"],
                verbose_I=verbose_I)
            # raw data files (i.e., mzML will be loaded dynamically)

            # load sequenceSegmentHandler files
            fileReaderOpenMS.load_quantitationMethods(
                sequenceSegmentHandler, sequenceHandler_IO.filenames[
                    "quantitationMethods_csv_i"],
                verbose_I=verbose_I)
            fileReaderOpenMS.load_standardsConcentrations(
                sequenceSegmentHandler, sequenceHandler_IO.filenames[
                    "standardsConcentrations_csv_i"],
                verbose_I=verbose_I)         
        else:  # load sequence from GUI
            pass
        
        # initialize the sequence
        self.groupSamplesInSequence(sequenceHandler_IO, sequenceSegmentHandler)
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
            # pass the same object that can be reused
            sample.raw_data = rawDataHandler_I

    def groupSamplesInSequence(self, sequenceHandler_IO, sequenceSegmentHandler_I=None):
        """group samples in a sequence

        An optional template SequenceSegmentHandler can be added to all groups
        
        Args:
            sequenceHandler_IO (SequenceHandler): sequence handler
            sequenceSegmentHandler_I (SequenceSegmentHandler): sequence group handler
        """

        sequence_groups_dict = {}
        for cnt, sample in enumerate(sequenceHandler_IO.sequence):
            if sample.meta_data["sequence_segment_name"] not in sequence_groups_dict.keys():
                sequence_groups_dict[sample.meta_data["sequence_segment_name"]] = []
            sequence_groups_dict[sample.meta_data["sequence_segment_name"]].append(cnt)
        
        sequence_groups = []
        for k, v in sequence_groups_dict.items():
            # pass a copy that can be edited
            if sequenceSegmentHandler_I is not None:
                sequenceSegmentHandler = copy.copy(sequenceSegmentHandler_I)
            else:
                sequenceSegmentHandler = SequenceSegmentHandler()
            sequenceSegmentHandler.sequence_segment_name = k
            sequenceSegmentHandler.sample_indices = v
            sequence_groups.append(sequenceSegmentHandler)

        sequenceHandler_IO.sequence_groups = sequence_groups

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
                        sample.meta_data["sample_type"])
                # if sample.raw_data.quantitation_methods is None:
                #     raw_data_processing_methods["quantify_peak"] = False
                    
            # process the samples
            for event in raw_data_processing_methods:
                rawDataProcessor.processRawData(
                    sample.raw_data,
                    event,
                    sequenceHandler_IO.parameters,
                    sequenceHandler_IO.getDefaultDynamicFilenames(
                        sequenceHandler_IO.getDirDynamic(),
                        sample.meta_data["sample_name"])
                    )

    def processSequenceSegments(
        self, sequenceHandler_IO,
        sample_names=[],
        sequence_segment_names=[],
        raw_data_processing_methods={},
        sequence_group_processing_methods={},
        verbose_I=False
    ):
        """process a sequence of samples by sequence groups
        
        Args:
            sequenceHandler_IO (SequenceHandler): the sequence class
            sample_names (list): name of the sample
            sequence_segment_names (list): name of the sequence group
            raw_data_process_methods (list): name of the raw data method to execute
            sequence_group_processing_methods (list): name of the sequence group
                method to execute
        """
        # classes
        seqGroupProcessor = SequenceSegmentProcessor()
        rawDataProcessor = RawDataProcessor()

        # process by sequence group
        for sequence_group in sequenceHandler_IO.sequence_groups:
            # 1: process all Standards
            sample_indices = seqGroupProcessor.getSampleIndicesBySampleType(
                sequenceSegmentHandler_I=sequence_group,
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
                    sequenceHandler_IO.getDefaultDynamicFilenames(
                        sequenceHandler_IO.getDirDynamic(),
                        sequenceHandler_IO.sequence[index].meta_data["sample_name"])
                    )
            # calculate the calibration curves
            seqGroupProcessor.optimizeCalibrationCurves(
                sequence_group, sequenceHandler_IO)
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
                sequenceSegmentHandler_I=sequence_group,
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
                    sequenceHandler_IO.getDefaultDynamicFilenames(
                        sequenceHandler_IO.getDirDynamic(),
                        sequenceHandler_IO.sequence[index].meta_data["sample_name"])
                    )
                # copy out the feature map
                sequenceHandler_IO.sequence[index].featureMap = \
                    sequenceHandler_IO.sequence[index].raw_data.featureMap

            # 3: process all QCs
            sample_indices = seqGroupProcessor.getSampleIndicesBySampleType(
                sequenceSegmentHandler_I=sequence_group,
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
                    sequenceHandler_IO.getDefaultDynamicFilenames(
                        sequenceHandler_IO.getDirDynamic(),
                        sequenceHandler_IO.sequence[index].meta_data["sample_name"])
                    )
                # copy out the feature map
                sequenceHandler_IO.sequence[index].featureMap = \
                    sequenceHandler_IO.sequence[index].raw_data.featureMap
            # # calculate the QCs
            # seqGroupProcessor.calculateQCs(
            #     sequence_group, sequenceHandler_IO)

            # 4: process all Blanks
            sample_indices = seqGroupProcessor.getSampleIndicesBySampleType(
                sequenceSegmentHandler_I=sequence_group,
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
                    sequenceHandler_IO.getDefaultDynamicFilenames(
                        sequenceHandler_IO.getDirDynamic(),
                        sequenceHandler_IO.sequence[index].meta_data["sample_name"])
                    )
                # copy out the feature map
                sequenceHandler_IO.sequence[index].featureMap = \
                    sequenceHandler_IO.sequence[index].raw_data.featureMap
            
            # 5: process all Double Blanks
            sample_indices = seqGroupProcessor.getSampleIndicesBySampleType(
                sequenceSegmentHandler_I=sequence_group,
                sequenceHandler_I=sequenceHandler_IO,
                sample_type="Double Blank"
            )
            for index in sample_indices:
                rawDataProcessor.processRawData(
                    sequenceHandler_IO.sequence[index].raw_data,
                    sequenceHandler_IO.sequence[index].raw_data_processing,
                    sequenceHandler_IO.parameters,
                    sequenceHandler_IO.getDefaultDynamicFilenames(
                        sequenceHandler_IO.getDirDynamic(),
                        sequenceHandler_IO.sequence[index].meta_data["sample_name"])
                    )

            # 6: process all Solvents
            sample_indices = seqGroupProcessor.getSampleIndicesBySampleType(
                sequenceSegmentHandler_I=sequence_group,
                sequenceHandler_I=sequenceHandler_IO,
                sample_type="Solvent"
            )
            for index in sample_indices:
                rawDataProcessor.processRawData(
                    sequenceHandler_IO.sequence[index].raw_data,
                    sequenceHandler_IO.sequence[index].raw_data_processing,
                    sequenceHandler_IO.parameters,
                    sequenceHandler_IO.getDefaultDynamicFilenames(
                        sequenceHandler_IO.getDirDynamic(),
                        sequenceHandler_IO.sequence[index].meta_data["sample_name"])
                    )
                # copy out the feature map
                sequenceHandler_IO.sequence[index].featureMap = \
                    sequenceHandler_IO.sequence[index].raw_data.featureMap
            # # calculate the carryover
            # seqGroupProcessor.calculateCarryover(
            #     sequence_group, sequenceHandler_IO)