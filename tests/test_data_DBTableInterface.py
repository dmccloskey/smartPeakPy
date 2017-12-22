# -*- coding: utf-8 -*-
from smartPeak.data.DBTableInterface import DBTableInterface
from smartPeak.data.DBConnection import DBConnection
from . import data_dir


class TestDBTableInterface():

    def __init__(self):

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

        self.db_table_interface = DBTableInterface(
            "sqlite3",
            "test1",
            None,
            ["test"],
            ["TEXT"],
            ["test1_unique"],
            ["UNIQUE(id, test)"]
        )
        self.db_table_interface.set_conn(conn)
        self.db_table_interface.set_cursor(cursor)

    def test_get_tableName(self):
        tbname = self.db_table_interface.get_tableName()
        assert(tbname == '"test1"')

    def test_get_tableColumns(self):
        colnames = self.db_table_interface.get_tableColumns()
        assert(colnames[0] == "id")
        assert(colnames[1] == "date_and_time") 
        assert(colnames[2] == "test")  

    def test_get_sequenceName(self):
        seqname = self.db_table_interface.get_sequenceName()
        assert(seqname == '"test1_id_seq"')

    def test_createAndDropTable(self):
        """Test methods for creating and dropping a table
        
        Methods tested:
            create_table
            drop_table
        """
        self.db_table_interface.drop_table()

        # override default values
        self.db_table_interface.create_table()
        
        query_I = '''INSERT INTO test1 (id, date_and_time, test) \
        VALUES (0, "now", "a");'''
        self.db_table_interface.execute_statement(query_I, raise_I=False, verbose_I=False)        
        query_I = '''INSERT INTO test1 (id, date_and_time, test) \
        VALUES (1, "now", "b");'''
        self.db_table_interface.execute_statement(query_I, raise_I=False, verbose_I=False)       
        query_I = '''INSERT INTO test1 (id, date_and_time, test) \
        VALUES (2, "now", "c");'''
        self.db_table_interface.execute_statement(query_I, raise_I=False, verbose_I=False)

        query_I = '''SELECT * FROM test1 ORDER BY id;'''
        result = self.db_table_interface.execute_select(
            query_I, 
            self.db_table_interface.get_tableColumns(),
            raise_I=False, verbose_I=False)
        assert(result[0]["test"] == "a")
        assert(result[1]["test"] == "b")
        assert(result[2]["test"] == "c")

        self.db_table_interface.drop_table()

        # use constraints
        self.db_table_interface.create_table()
        
        query_I = '''INSERT INTO test1 (test) VALUES ("a");'''
        self.db_table_interface.execute_statement(query_I, raise_I=False, verbose_I=False)        
        query_I = '''INSERT INTO test1 (test) VALUES ("b");'''
        self.db_table_interface.execute_statement(query_I, raise_I=False, verbose_I=False)       
        query_I = '''INSERT INTO test1 (test) VALUES ("c");'''
        self.db_table_interface.execute_statement(query_I, raise_I=False, verbose_I=False)

        query_I = '''SELECT * FROM test1 ORDER BY id;'''
        result = self.db_table_interface.execute_select(
            query_I, 
            self.db_table_interface.get_tableColumns(),
            raise_I=False, verbose_I=False)
        assert(result[0]["test"] == "a")
        assert(result[1]["test"] == "b")
        assert(result[2]["test"] == "c")
        assert(result[0]["id"] == 1)
        assert(result[1]["id"] == 2)
        assert(result[2]["id"] == 3)

        self.db_table_interface.drop_table()