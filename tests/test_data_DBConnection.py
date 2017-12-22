# -*- coding: utf-8 -*-
from smartPeak.data.DBConnection import DBConnection
from . import data_dir


class TestDBConnection():

    def test_DBConnection(self, test_postgresql=False, test_sqlite=True):
        """Tests all methods in DBConnection"""
        db_connection = DBConnection()

        # test postgresql
        if test_postgresql:
            pg_settings = {"database": {
                "dialect": "postgresql",
                "host": "localhost",
                "database": "postgres",
                "password": "postgres",
                "schema": "public",
                "user": "postgres"
            }}
            db_connection.set_conn(pg_settings['database'])
            conn = db_connection.get_conn()
            assert(conn is not None)
            db_connection.set_cursor(pg_settings['database'])
            cursor = db_connection.get_cursor()
            assert(cursor is not None)

        # sqlite
        if test_sqlite:
            pg_settings = {"database": {
                "dialect": "sqlite3",
                "host": data_dir + "sqlite_test.db",
                "database": "",
                "password": "",
                "schema": "",
                "user": ""
            }}
            db_connection.set_conn(pg_settings['database'])
            conn = db_connection.get_conn()
            assert(conn is not None)
            db_connection.set_cursor(pg_settings['database'])
            cursor = db_connection.get_cursor()
            assert(cursor is not None)
