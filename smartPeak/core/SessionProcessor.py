# -*- coding: utf-8 -*-


class SessionProcessor():

    def loadSession(
        self, 
        sequence_handler_IO,
        session_filename
    ):
        """Load all assets associated with the session from
        a session file

        Args:
            sequence_handler_IO (SequenceHandler): the sequence class
            session_filename (str): the name of the session file

        """
    
    def storeSession(self, session_filename):
        """Write the current session to file"""

    def createSession(self, filenames={}):
        """Create a new session from file"""

    def undo(self):
        """Step back 1 step in the session history"""

    def redo(self):
        """Step forward 1 step in the session history after
        calling one or more undo commands"""