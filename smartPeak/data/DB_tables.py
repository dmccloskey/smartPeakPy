# -*- coding: utf-8 -*-
from .DB_io import DB_io


class DB_table_interface(DB_io):
    """DB table interface
    
    All DB table classes should inherit this object
    """
    def __init__(self, table_name):
        self.table_name = table_name

    def create_table(self):
        pass

    def add_row(self, row):
        """Add a table row
        
        Args:
            row (dict): key, value pair where key is the column name and value is the column value
        
        """
        pass

    def add_rows(self, rows):
        """Add a table row
        
        Args:
            rows (list): list of key, value pairs
        
        """
        pass

    def update_rows(self):
        """Update table rows"""
        pass

    def delete_rows(self):
        """Delete table rows"""
        pass

    def select_rows(self):
        """Select table rows"""
        pass


class DB_table_handler():
    """DB table handler
    
    All DB table objects should be called through this handler
    """
    def __init__(self, table_obj):
        self.table_obj = table_obj

    def create_table(self):
        self.table_obj.create_table()

    def add_rows(self, rows):
        self.table_obj.add_rows(rows)

    def update_rows(self):
        self.table_obj.update_rows()

    def delete_rows(self):
        self.table_obj.delete_rows()

    def select_rows(self):
        self.table_obj.select_rows()
