# -*- coding: utf-8 -*-
from smartPeak.data.DBio import DBio
from smartPeak.data.DBConnection import DBConnection
from . import data_dir


class TestDBio():

    def test_convert_list2string(self):
        db_io = DBio()

        test = ["a","b","c"]
        test_str = db_io.convert_list2string(test)
        assert(test_str == "a,b,c")

        test = "a,b,c"
        test_str = db_io.convert_list2string(test)
        assert(test_str == "a,b,c")

    def test_merge_keysAndListOfTuplest(self):
        db_io = DBio()
        columns = ["id", "test"]
        rows = [
            (0, "a"),
            (1, "b"),
            (2, "c")
            ]
        result = db_io.merge_keysAndListOfTuples(columns, rows)
        assert(result[0]["id"] == 0)
        assert(result[0]["test"] == "a")
        assert(result[2]["id"] == 2)
        assert(result[2]["test"] == "c")

    def test_execute_statement(self):
        # connect to the DB
        pg_settings = {"database": {
            "dialect": "sqlite3",
            "host": data_dir + "sqlite_test.db",
            "database": "",
            "password": "",
            "schema": "",
            "user": ""
        }}
        db_connection = DBConnection()
        db_connection.set_conn(pg_settings['database'])
        conn = db_connection.get_conn()
        db_connection.set_cursor(pg_settings['database'])
        cursor = db_connection.get_cursor()

        # query against the DB
        db_io = DBio(cursor, conn)    

        query_I = '''DROP TABLE IF EXISTS test1;'''
        db_io.execute_statement(query_I, raise_I=False, verbose_I=False)

        query_I = '''CREATE TABLE IF NOT EXISTS test1 (id INTEGER, test TEXT);'''
        db_io.execute_statement(query_I, raise_I=False, verbose_I=False)

        columns = ["id", "test"]
        
        query_I = '''INSERT INTO test1 (id, test) VALUES (0, "hello");'''
        db_io.execute_statement(query_I, raise_I=False, verbose_I=False)

        query_I = '''SELECT %s FROM test1 WHERE id=0;''' % (
            db_io.convert_list2string(columns)
        )
        result = db_io.execute_select(query_I, columns, raise_I=False, verbose_I=False)
        assert(result[0]["test"] == "hello")

        query_I = '''UPDATE test1 SET test="goodbye" WHERE id=0;'''
        db_io.execute_statement(query_I, raise_I=False, verbose_I=False)        

        query_I = '''SELECT %s FROM test1 WHERE id=0;''' % (
            db_io.convert_list2string(columns)
        )
        result = db_io.execute_select(query_I, columns, raise_I=False, verbose_I=False)
        assert(result[0]["test"] == "goodbye")

        query_I = '''DELETE FROM test1 WHERE id=0;'''
        db_io.execute_statement(query_I, raise_I=False, verbose_I=False)        

        query_I = '''SELECT %s FROM test1 WHERE id=0;''' % (
            db_io.convert_list2string(columns)
        )
        result = db_io.execute_select(query_I, columns, raise_I=False, verbose_I=False)
        assert(len(result) == 0)

        query_I = '''DROP TABLE IF EXISTS test1;'''
        db_io.execute_statement(query_I, raise_I=False, verbose_I=False)        

        query_I = '''SELECT %s FROM test1 WHERE id=0;''' % (
            db_io.convert_list2string(columns)
        )
        result = db_io.execute_select(query_I, columns, raise_I=False, verbose_I=False)
        assert(result is None)