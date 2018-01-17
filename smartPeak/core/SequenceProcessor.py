# -*- coding: utf-8 -*-
from .SequenceGroupProcessor import SequenceGroupProcessor
from smartPeak.io.SequenceReader import SequenceReader
from smartPeak.io.FileReader import FileReader
from smartPeak.io.FileReaderOpenMS import FileReaderOpenMS


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
            filenames (dict): map of filetype to filename
        """

        if filenames:  # load sequence from disk files 

            # read in the sequence file
            seqReader = SequenceReader()
            seqReader.read_sequenceFile(
                sequenceHandler_IO, filenames["sequence"], delimiter)

            # read in the parameters
            fileReader = FileReader()
            fileReader.read_openMSParams(filenames["parameters"], delimiter)
            params = fileReader.getData()
            fileReader.clear_data()

            # check for workflow parameters integrity
            required_parameters = [
                "MRMMapping",
                "ChromatogramExtractor", "MRMFeatureFinderScoring",
                "MRMFeatureFilter.filter_MRMFeatures",
                "MRMFeatureSelector.select_MRMFeatures_qmip",
                "MRMFeatureSelector.schedule_MRMFeatures_qmip",
                "MRMFeatureSelector.select_MRMFeatures_score",
                "ReferenceDataMethods.getAndProcess_referenceData_samples",
                "MRMFeatureValidator.validate_MRMFeatures",
                "MRMFeatureFilter.filter_MRMFeatures.qc",
            ]
            for parameter in required_parameters:
                if parameter not in params:
                    params[parameter] = []
            sequenceHandler_IO.parameters = params

            # load rawDataHandler files (applies to the whole session)
            fileReaderOpenMS = FileReaderOpenMS()
            fileReaderOpenMS.load_TraML(
                sequenceHandler_IO, filenames, verbose_I=verbose_I)
            fileReaderOpenMS.load_featureFilter(
                sequenceHandler_IO, filenames, verbose_I=verbose_I)
            fileReaderOpenMS.load_featureQC(
                sequenceHandler_IO, filenames, verbose_I=verbose_I)
            # raw data files (i.e., mzML will be loaded dynamically)

            # load sequenceGroupHandler files
            fileReaderOpenMS.load_quantitationMethods(
                sequenceHandler_IO, filenames, verbose_I=verbose_I)
            fileReaderOpenMS.load_standardsConcentrations(
                sequenceHandler_IO, filenames, verbose_I=verbose_I)            

    def processSequence(
        self, sequenceHandler_IO,
        sample_names=[],
        sequence_group_names=[],
        raw_data_processing_methods={},
        sequence_group_processing_methods={}
    ):
        """process a sequence of samples
        
        Args:
            sequenceHandler_IO (SequenceHandler): the sequence class
            sample_names (list): name of the sample
            sequence_group_names (list): name of the sequence group
            raw_data_process_methods (list): name of the raw data method to execute
            sequence_group_processing_methods (list): name of the sequence method to execute            
        """
        # classes
        seqGroupProcessor = SequenceGroupProcessor()
        rawDataHandler = rawDataHandler()
        rawDataProcessor = RawDataProcessor()
        fileReaderOpenMS = FileReaderOpenMS()

        # process by sequence group
        for sequence_group in sequenceHandler_IO.sequence_groups:
            # 1: process all Standards
            sample_indices = seqGroupProcessor.getSampleIndicesBySampleType(
                sequenceGroupHandler_I=sequence_group,
                sequenceHandler_I=sequenceHandler_IO,
                sample_type="Standard"
            )
            # process the raw data
            for index in sample_indices:
                self.processRawData(
                    sequenceHandler_IO.sequence[index], raw_data_processing_methods)
            # calculate the calibration curves
            calibrators = []
            for index in sample_indices:
                if sequenceHandler_IO.sequence[index].raw_data_processing == "calculate_calibration":
                    calibrators.append(sequenceHandler_IO.sequence[index])  # where is the actual concentrations?

            # 2: process all Unknowns
            # 3: process all Blanks, Double Blanks, and Solvents

