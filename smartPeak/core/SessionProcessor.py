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
        pass
    
    def storeSession(self, session_name, session_dir):
        """Write the current session to file
        
        All loaded data will be converted to tabular form
        and then inserted/updated in the session file

        Args:
            session_name (str): name of the session file
            session_dir (str): directory of the session
        """
        pass

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
            pass
        else:  # create session using the wizard     
            pass

    def undo(self):
        """Step back 1 step in the session history"""
        pass

    def redo(self):
        """Step forward 1 step in the session history after
        calling one or more undo commands"""
        pass