# -*- coding: utf-8 -*-


class SessionHandler():

    def __init__(self):
        """Session
        """

        self.session_filename = None
        self.dynamic_load_session = None
        self.dynamic_load_data = None
        self.transaction_log = None

    def clear_data(self):
        self.session_filename = None
        self.dynamic_load_session = None
        self.dynamic_load_data = None
        self.transaction_log = None