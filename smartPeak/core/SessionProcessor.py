# -*- coding: utf-8 -*-
from smartPeak.io.SequenceReader import SequenceReader
from smartPeak.io.FileReader import FileReader
from smartPeak.io.FileReaderOpenMS import FileReaderOpenMS


class SessionProcessor():

    def loadSession(
        self, 
        sequence_handler_IO,
        session_name, session_dir
    ):
        """Load all assets associated with the session from
        a session file

        Args:
            session_name (str): name of the session file
            session_dir (str): directory of the session

        """
    
    def storeSession(self, session_name, session_dir):
        """Write the current session to file
        
        All loaded data will be converted to tabular form
        and then inserted/updated in the session file

        Args:
            session_name (str): name of the session file
            session_dir (str): directory of the session
        """

    def createSession(
        self, 
        sessionHandler_IO, 
        sequenceHandler_IO, 
        filenames={}, 
        verbose_I=False
    ):
        """Create a new session from files or wizard
        
        Args:
            filenames (dict): map of filetype to filename
        """

        if filenames:  # load session from disk files 
            delimiter = ","
            crateSequence

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

            # load session files (applies to the whole session)
            fileReaderOpenMS = FileReaderOpenMS()
            fileReaderOpenMS.load_TraML(
                sessionHandler_IO, filenames, verbose_I=verbose_I)
            fileReaderOpenMS.load_featureFilter(
                sessionHandler_IO, filenames, verbose_I=verbose_I)
            fileReaderOpenMS.load_featureQC(
                sessionHandler_IO, filenames, verbose_I=verbose_I)

            # load sequenceGroupHandler files
            fileReaderOpenMS.load_quantitationMethods(
                sessionHandler_IO, filenames, verbose_I=verbose_I)
            fileReaderOpenMS.load_standardsConcentrations(
                sessionHandler_IO, filenames, verbose_I=verbose_I)

            # raw data files (i.e., mzML will be loaded dynamically)

        else:  # create session using the wizard     
            pass

    def undo(self):
        """Step back 1 step in the session history"""

    def redo(self):
        """Step forward 1 step in the session history after
        calling one or more undo commands"""