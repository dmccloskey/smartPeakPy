# -*- coding: utf-8 -*-
from smartPeak.data.DBConnection import DBConnection
from . import data_dir


class testDBConnection():

    def test_set_conn(self, test_postgresql=False, test_sqlite=True):
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
            db_connection.set_cursor(pg_settings['database'])
            cursor = db_connection.get_cursor()
            conn = db_connection.get_conn()
            assert(cursor is not None)
            assert(conn is not None)

        # sqlite
            pg_settings = {"database": {
                "dialect": "sqlite",
                "host": data_dir + "sqlite_test.db",
                "database": "",
                "password": "",
                "schema": "",
                "user": ""
            }}
            db_connection.set_conn(pg_settings['database'])
            db_connection.set_cursor(pg_settings['database'])
            cursor = db_connection.get_cursor()
            conn = db_connection.get_conn()
            assert(cursor is not None)
            assert(conn is not None)
