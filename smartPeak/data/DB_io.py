# -*- coding: utf-8 -*-
try:
    from sqlalchemy.dialects import postgresql
    from sqlalchemy.exc import SQLAlchemyError
except ImportError as e:
    print(e)

class DB_io():
    def __init__(self, session_I=None, engine_I=None, settings_I={}, data_I=None):
        # base properties
        if session_I: 
            self.session = session_I
        else: 
            self.session = None
        if engine_I: 
            self.engine = engine_I
        else: 
            self.engine = None
        if settings_I: 
            self.settings = settings_I
        else: 
            self.settings = {}
        if data_I: 
            self.data = data_I
        else: 
            self.data = []

    def set_session(self, session_I):
        '''set the session object'''
        self.session = session_I

    def set_engine(self, engine_I):
        '''set the engine object'''
        self.engine = engine_I

    def set_settings(self, settings_I):
        '''set the settings object'''
        self.settings = settings_I

    def get_session(self, session_I):
        '''get the session object'''
        self.session = session_I

    def get_engine(self, engine_I):
        '''get the engine object'''
        self.engine = engine_I

    def get_settings(self, settings_I):
        '''get the settings object'''
        self.settings = settings_I

    def clear_data(self):
        '''clear the data cache'''
        del self.data[:]

    def set_data(self, data_I):
        '''set data'''
        self.data = data_I

    def add_data(self, data_I):
        '''add data'''
        self.data.extend(data_I)

    def get_data(self):
        '''get the data cache'''
        return self.data

    def convert_list2string(self, list_I, deliminator_I=','):
        '''convert a list 2 a string

        Args:
            list_I (list)
            deliminator_I (str)
        
        Returns:
            string: string_O
        '''
        string_O = ''
        if isinstance(list_I, list):
            string_O = deliminator_I.join(list_I)
        elif isinstance(list_I, str):
            string_O = list_I
        else:
            print('type of list_I is not supported.')
        return string_O

    def execute_select(self, query_I, raise_I=False):
        '''execute a raw sql query

        Args:
            query_I (str): string or sqlalchemy text or sqlalchemy select
            raise_I (boolean): boolean, raise error

        Returns:
            tuple: data_O: keyed tuple sqlalchemy object
        '''
        data_O = None
        try:
            ans = self.session.execute(query_I)
            data_O = ans.fetchall()  # TODO: export direction to listDict object
        except SQLAlchemyError as e:
            self.session.rollback()
            if raise_I:
                raise
            else: 
                print(e)
        return data_O