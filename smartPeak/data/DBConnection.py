# -*- coding: utf-8 -*-
import sqlite3
import psycopg2
import psycopg2.extras


class DBConnection():
    def __init__(self):
        self.conn = None
        self.cursor = None

    def set_conn(self, settings_I={}):
        '''Set connection to the database

        Args:
            settings_I (dict): a dictionary of settings e.g., settings name:settings value

        '''
        conn = None
        try:
            if "dialect" not in settings_I.keys():
                raise Exception('dialect not specified.')
            if settings_I["dialect"] == "postgresql":
                conn_string = "dbname='%s' user='%s' host='%s' password='%s'" % (
                    settings_I['database'], settings_I['password'], 
                    settings_I['host'], settings_I['user'])
                conn = psycopg2.connect(conn_string)
            elif settings_I["dialect"] == "sqlite3":
                conn_string = "%s" % (settings_I['host'])
                conn = sqlite3.connect(conn_string)
        except Exception as e:
            print(e)
            exit(-1)
        self.conn = conn

    def get_conn(self):
        '''return connection to the database
        '''
        return self.conn

    def set_cursor(self, settings_I):
        '''Set a cursor to the database

        Args:
            settings_I (dict): a dictionary of settings e.g., settings name:settings value
        '''
        cursor = None
        try:
            if "dialect" not in settings_I.keys():
                raise Exception('dialect not specified.')
            if settings_I["dialect"] == "postgresql":
                # cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor = self.conn.cursor()
            elif settings_I["dialect"] == "sqlite3":
                cursor = self.conn.cursor()
        except Exception as e:
            print(e)
        self.cursor = cursor

    def get_cursor(self):
        '''return new session object'''
        return self.cursor