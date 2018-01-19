# -*- coding: utf-8 -*-


class SessionHandler():

    def __init__(self):
        """Session
        """

        self.session_id = None
        self.session_name = None
        self.session_dir = None
        self.dynamic_load_session = None
        self.dynamic_load_data = None

        self.filenames = None

        # Log of all session transactions
        self.transaction_log = None
        # Location of the current session in the 
        # transaction log
        self.transaction_index = None  
        # The number of recorded processes
        self.transaction_limit = None  

        self.targeted = None
        self.reference_data = None
        self.quantitation_methods = None
        self.feature_filter = None
        self.feature_qc = None
        self.standards_concentrations = None

    def clear_data(self):
        pass