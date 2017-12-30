# -*- coding: utf-8 -*-
from smartPeak.data.DBTableInterface import DBTableInterface
from smartPeak.data.DBConnection import DBConnection
from smartPeak.data.DBio import DBio
from smartPeak.data.DBTables import DBTables
from . import data_dir


class TestDBTableInterface():

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

        # test that all tables were made
        tables = [
            "sequence_file", "traml", "feature_filter", 
            "feature_qc", "feature_maps", "quantitation_methods", 
            "standards_concentrations", "undolog"]
        for table in tables:
            query = """SELECT COUNT(*) from sqlite_master
            where type='table' and name='%s'""" % (
                table)
            result = dbtables.undolog.execute_select(query)
            assert(result == 1)
            
        # test table constraints
