# -*- coding: utf-8 -*-


class DBTableHandler():
    """DB table handler
    
    All DB table objects should be called through this handler
    """
    def __init__(self, table_obj):
        self.table_obj_ = table_obj

    def create_table(self):
        self.table_obj_.create_table()

    def add_rows(self, rows):
        self.table_obj_.add_rows(rows)

    def update_rows(self):
        self.table_obj_.update_rows()

    def delete_rows(self):
        self.table_obj_.delete_rows()

    def select_rows(self):
        self.table_obj_.select_rows()