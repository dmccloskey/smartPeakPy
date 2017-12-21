# -*- coding: utf-8 -*-
from .DBio import DBio


class DBTableInterface(DBio):
    """DB table interface
    
    All DB table classes should inherit this object
    """
    def __init__(self, table_name):
        self.table_name_ = table_name

    def create_table(self):
        pass

    def add_row(self, row):
        """Add a table row
        
        Args:
            row (dict): key, value pair where key is the column name and
                value is the column value
        
        """
        insert_cols = ""
        insert_vals = ""
        for k, v in row.items():
            insert_cols = '''"%s", ''' % (k)
            insert_vals = '''%s, ''' % (v)
        insert_cols = insert_cols[-2]
        insert_vals = insert_vals[-2]
        cmd = """INSERT INTO %s (%s) values (%s);""" % (
            self.table_name_, insert_cols, insert_vals)
        self.execute_statement(cmd)

    def add_rows(self, rows):
        """Add a table row
        
        Args:
            rows (list): list of key, value pairs
        
        """
        for row in rows:
            self.add_row(row)

    def update_rows(self):
        """Update table rows"""
        pass

    def delete_rows(self):
        """Delete table rows"""
        pass

    def select_rows(self):
        """Select table rows"""
        pass
