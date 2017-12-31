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

    def get_cursor(self):
        '''get the cursor object'''
        return self.cursor

    def get_conn(self):
        '''get the conn object'''
        return self.conn

    def get_settings(self):
        '''get the settings object'''
        return self.settings

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

    def merge_keysAndListOfTuples(self, keys, list):
        '''convert a list of tuple to a list of dicts

        NOTE: order of keys and values must match!

        Args:
            keys (list): list of keys
            list (list): list of tuples with values
        
        Returns:
            list_O: list of dicts
        '''
        list_O = [dict(zip(keys, row)) for row in list]
        return list_O

    def execute_select(self, query_I, columns=None, raise_I=False, verbose_I=False):
        '''execute a raw sql select

        Args:
            query_I (str): string or sqlalchemy text or sqlalchemy select
            columns (list): list of expected column names (if applicable)
            raise_I (bool): boolean, raise error
            verbose_I (bool): boolean, print query statement

        Returns:
            tuple: data_O: keyed tuple sqlalchemy object
        '''
        data_O = None
        try:
            if verbose_I:
                print(query_I)
            self.cursor.execute(query_I)
            data_O = self.cursor.fetchall()
            if columns is not None:
                data_O = self.merge_keysAndListOfTuples(columns, data_O)
        except Exception as e:
            self.conn.rollback()
            if raise_I:
                raise
            else: 
                print(e)
        return data_O

    def execute_statement(self, query_I, raise_I=False, verbose_I=False):
        '''execute a raw sql insert, update, or delete
        
        Args:
            query_I (str): string or sqlalchemy text
            raise_I (bool): boolean, raise error
            verbose_I (bool): boolean, print query statement

        '''
        try:
            if verbose_I:
                print(query_I)
            self.cursor.execute(query_I)
            if self.cursor == 0:
                print("No rows changed.")
            else:
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            if raise_I: 
                raise
            else: 
                print(e)