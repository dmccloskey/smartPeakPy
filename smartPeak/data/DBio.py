# -*- coding: utf-8 -*-


class DBio():
    def __init__(self, cursor_I=None, conn_I=None, settings_I={}, data_I=None):
        # base properties
        if cursor_I: 
            self.cursor = cursor_I
        else: 
            self.cursor = None
        if conn_I: 
            self.conn = conn_I
        else: 
            self.conn = None
        if settings_I: 
            self.settings = settings_I
        else: 
            self.settings = {}
        if data_I: 
            self.data = data_I
        else: 
            self.data = []

    def set_cursor(self, cursor_I):
        '''set the cursor object'''
        self.cursor = cursor_I

    def set_conn(self, conn_I):
        '''set the conn object'''
        self.conn = conn_I

    def set_settings(self, settings_I):
        '''set the settings object'''
        self.settings = settings_I

    def get_cursor(self, cursor_I):
        '''get the cursor object'''
        self.cursor = cursor_I

    def get_conn(self, conn_I):
        '''get the conn object'''
        self.conn = conn_I

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
        '''execute a raw sql select

        Args:
            query_I (str): string or sqlalchemy text or sqlalchemy select
            raise_I (boolean): boolean, raise error

        Returns:
            tuple: data_O: keyed tuple sqlalchemy object
        '''
        data_O = None
        try:
            self.cursor.execute(query_I)
            data_O = self.cursor.fetchall()
        except Exception as e:
            self.conn.rollback()
            if raise_I:
                raise
            else: 
                print(e)
        return data_O

    def execute_statement(self, query_I, raise_I=False):
        '''execute a raw sql insert, update, or delete
        
        Args:
            query_I (str): string or sqlalchemy text
            raise_I (bool): boolean, raise error

        '''
        try:
            self.cursor.execute(query_I)
            if self.cursor == 0:
                print("No rows changed.")
            else:
                self.cursor.commit()
        except Exception as e:
            self.conn.rollback()
            if raise_I: 
                raise
            else: 
                print(e)