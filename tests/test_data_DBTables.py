# -*- coding: utf-8 -*-
from smartPeak.data.DBTableInterface import DBTableInterface
from smartPeak.data.DBConnection import DBConnection
from smartPeak.data.DBio import DBio
from smartPeak.data.DBTables import DBTables
from . import data_dir


class TestDBTables():

    def test_set_tables(self):    

        # settings    
        pg_settings = {"database": {
            "dialect": "sqlite3",
            "host": data_dir + "sqlite_test.db",
            "database": "",
            "password": "",
            "schema": "",
            "user": ""
        }}

        # set the tables
        dbtables = DBTables()
        dbtables.set_tables(pg_settings)
        tbname = dbtables.sequence_file.get_tableName()
        assert(tbname == '"sequence_file"')

        tbname = dbtables.traml.get_tableName()
        assert(tbname == '"traml"')

        tbname = dbtables.feature_filter.get_tableName()
        assert(tbname == '"feature_filter"')

        tbname = dbtables.feature_qc.get_tableName()
        assert(tbname == '"feature_qc"')

        tbname = dbtables.feature_maps.get_tableName()
        assert(tbname == '"feature_maps"')

        tbname = dbtables.quantitation_methods.get_tableName()
        assert(tbname == '"quantitation_methods"')

        tbname = dbtables.standards_concentrations.get_tableName()
        assert(tbname == '"standards_concentrations"')

        tbname = dbtables.undolog.get_tableName()
        assert(tbname == '"undolog"')

    def test_get_table(self):

        # settings    
        pg_settings = {"database": {
            "dialect": "sqlite3",
            "host": data_dir + "sqlite_test.db",
            "database": "",
            "password": "",
            "schema": "",
            "user": ""
        }}

        # set the tables
        dbtables = DBTables()
        dbtables.set_tables(pg_settings)

        tbname = dbtables.get_table("sequence_file").get_tableName()
        assert(tbname == '"sequence_file"')

        tbname = dbtables.get_table("traml").get_tableName()
        assert(tbname == '"traml"')

        tbname = dbtables.get_table("feature_filter").get_tableName()
        assert(tbname == '"feature_filter"')

        tbname = dbtables.get_table("feature_qc").get_tableName()
        assert(tbname == '"feature_qc"')

        tbname = dbtables.get_table("feature_maps").get_tableName()
        assert(tbname == '"feature_maps"')

        tbname = dbtables.get_table("quantitation_methods").get_tableName()
        assert(tbname == '"quantitation_methods"')

        tbname = dbtables.get_table("standards_concentrations").get_tableName()
        assert(tbname == '"standards_concentrations"')

        tbname = dbtables.get_table("undolog").get_tableName()
        assert(tbname == '"undolog"')

    def test_connect_tables(self):

        # settings    
        pg_settings = {"database": {
            "dialect": "sqlite3",
            "host": data_dir + "sqlite_test.db",
            "database": "",
            "password": "",
            "schema": "",
            "user": ""
        }}

        # set the tables
        dbtables = DBTables()
        dbtables.set_tables(pg_settings)
        dbtables.connect_tables(pg_settings)

        # test conn
        conn = dbtables.sequence_file.get_conn()
        assert(conn is not None)

        conn = dbtables.traml.get_conn()
        assert(conn is not None)

        conn = dbtables.feature_filter.get_conn()
        assert(conn is not None)

        conn = dbtables.feature_qc.get_conn()
        assert(conn is not None)

        conn = dbtables.feature_maps.get_conn()
        assert(conn is not None)

        conn = dbtables.quantitation_methods.get_conn()
        assert(conn is not None)

        conn = dbtables.standards_concentrations.get_conn()
        assert(conn is not None)

        conn = dbtables.undolog.get_conn()
        assert(conn is not None)
        
        # test cursor
        cursor = dbtables.sequence_file.get_cursor()
        assert(cursor is not None)

        cursor = dbtables.traml.get_cursor()
        assert(cursor is not None)

        cursor = dbtables.feature_filter.get_cursor()
        assert(cursor is not None)

        cursor = dbtables.feature_qc.get_cursor()
        assert(cursor is not None)

        cursor = dbtables.feature_maps.get_cursor()
        assert(cursor is not None)

        cursor = dbtables.quantitation_methods.get_cursor()
        assert(cursor is not None)

        cursor = dbtables.standards_concentrations.get_cursor()
        assert(cursor is not None)

        cursor = dbtables.undolog.get_cursor()
        assert(cursor is not None)

    def test_createAndDrop_tables(self):    
        """Tests the creating and dropping tables defined in DBTables
        
        The following methods are tested
        connect_tables
        create_tables
        drop_tables
        """

        # settings    
        pg_settings = {"database": {
            "dialect": "sqlite3",
            "host": data_dir + "sqlite_test.db",
            "database": "",
            "password": "",
            "schema": "",
            "user": ""
        }}

        # set the tables
        dbtables = DBTables()
        dbtables.set_tables(pg_settings)
        dbtables.connect_tables(pg_settings)
        dbtables.create_tables()

        # test that all tables were made
        tables = [
            "sequence_file", "traml", "feature_filter", 
            "feature_qc", "feature_maps", "quantitation_methods", 
            "standards_concentrations", "undolog"]
        for table in tables:
            print("Testing existance of table " + table)
            query = """SELECT COUNT(*) from sqlite_master
            where type='table' and name='%s'""" % (
                table)
            result = dbtables.undolog.execute_select(query)
            assert(result[0][0] == 1)

        # test table constraints
        default_data = {"TEXT": "'a'", "INTEGER": 1, "REAL": 1.0}
        tables1 = [
            "sequence_file", "traml", "feature_filter", 
            "feature_qc", "feature_maps", "quantitation_methods", 
            "standards_concentrations"]
        for table in tables1:
            print("Testing constraints for table " + table)
            columns = dbtables.get_table(table).get_tableColumns()[2:]
            data_types = dbtables.get_table(table).get_tableDataTypes()[2:]
            defaults = [default_data[d] for d in data_types]
            row1 = dict(zip(columns, defaults))
            row2 = dict(zip(columns, defaults))
            rows = [row1, row2]
            try:
                dbtables.get_table(table).insert_rows(rows, raise_I=True)
            except Exception as e:
                # test that the UNIQUE constraint failed
                assert(e.args[0].find("UNIQUE") == 0)
        tables2 = ["undolog"]
        for table in tables2:
            print("Testing constraints for table " + table)
            columns = dbtables.get_table(table).get_tableColumns()[2:]
            data_types = dbtables.get_table(table).get_tableDataTypes()[2:]
            defaults = [default_data[d] for d in data_types]
            row1 = dict(zip(columns, defaults))
            row2 = dict(zip(columns, defaults))
            rows = [row1, row2]
            # test that no constraints failed
            dbtables.get_table(table).insert_rows(rows, raise_I=True)        

        # drop the tables
        dbtables.drop_tables()

        # test that all tables were removed
        tables = [
            "sequence_file", "traml", "feature_filter", 
            "feature_qc", "feature_maps", "quantitation_methods", 
            "standards_concentrations", "undolog"]
        for table in tables:
            print("Dropping table " + table)
            query = """SELECT COUNT(*) from sqlite_master
            where type='table' and name='%s'""" % (
                table)
            result = dbtables.undolog.execute_select(query)
            assert(result[0][0] == 0)

