# -*- coding: utf-8 -*-
from .DBio import DBio


class DBTableInterface(DBio):
    """DB table interface
    
    All DB table classes should inherit this object
    """
    def __init__(
        self, dialect, table_name, schema_name, 
        columns, data_types, constraints
    ):
        """Initialize all attributes
        
        Args:
            dialect (str): dialect e.g., postgresql, sqlite, etc.,
            table_name (str): name of the table
            schema_name (str): name of the schema that the table belongs
            columns (list): list of column names
            data_types (list): list of data types that match the list of column names
            constraints (list): list of sql text constraints
        """
        self.dialect_ = dialect
        self.table_name_ = table_name
        self.schema_name_ = schema_name
        self.columns_ = columns
        self.data_types_ = data_types
        self.constraints_ = constraints
        assert(len(self.columns_ == self.data_types_))

    def get_tableName(self):
        """Return a table name"""
        table_name = ""
        if self.schema_name_ is not None:
            table_name = '''"%s".''' % (self.schema_name_)
        table_name += '''"%s"''' % (self.table_name_)
        return table_name

    def create_table(self, initialize_pkey_I=True, raise_I=False):
        """Create a table"""
        try:
            # make the table
            col_type_stmt = ""
            if initialize_pkey_I:
                col_type_stmt += '''id INT NOT NULL CONSTRAINT 
                "%s_pkey" PRIMARY KEY (id), ''' % (
                    self.table_name_
                ) 
            for i in range(len(self.columns_)):
                col_type_stmt = '''"%s" %s, ''' % (
                    self.columns_[i], 
                    self.data_types_[i], 
                )
            col_type_stmt = col_type_stmt[-2]
            cmd = """CREATE TABLE %s (%s)""" % (
                self.get_tableName(), col_type_stmt)
            self.execute_statement(cmd)

            # make the indexes

            # make the constraints

        except Exception as e:
            if raise_I:
                raise
            else: 
                print(e)

    def drop_table(self, raise_I=False):
        """Drop a table"""
        try:
            cmd = """DROP TABLE %s;""" % (
                self.get_tableName())
            self.execute_statement(cmd)
        except Exception as e:
            if raise_I:
                raise
            else: 
                print(e)

    def alter_table(self, alter_stm, raise_I=False):
        """Alter a table
        
        Args:
            alter_stm (str): alter clause
        
        """
        try:
            cmd = 'ALTER TABLE IF EXISTS %s %s' % (
                self.get_tableName(), alter_stm)
            self.execute_statement(cmd)
        except Exception as e:
            if raise_I:
                raise
            else: 
                print(e)

    def create_index(self, raise_I=False):
        """TODO"""

    def drop_index(self, raise_I=False):
        """TODO"""

    def create_trigger(self, raise_I=False):
        """TODO"""

    def drop_drop(self, raise_I=False):
        """TODO"""

    def add_row(self, col_val, raise_I=False):
        """Add a table row
        
        Args:
            col_val (dict): key, value pair where key is the column name and
                value is the column value
        
        """
        try:
            insert_cols = ""
            insert_vals = ""
            for k, v in col_val.items():
                insert_cols = '''"%s", ''' % (k)
                insert_vals = '''%s, ''' % (v)
            insert_cols = insert_cols[-2]
            insert_vals = insert_vals[-2]
            cmd = """INSERT INTO %s (%s) VALUES (%s);""" % (
                self.get_tableName(), insert_cols, insert_vals)
            self.execute_statement(cmd)
        except Exception as e:
            if raise_I:
                raise
            else: 
                print(e)

    def add_rows(self, rows, raise_I=False):
        """Add a table row
        
        Args:
            rows (list): list of key, value pairs
        
        """
        try:
            for row in rows:
                self.add_row(row)
        except Exception as e:
            if raise_I:
                raise
            else: 
                print(e)

    def update_rows(self, col_val, where_stm, raise_I=False):
        """Update table rows
        
        Args:
            col_val (dict): key, value pair where key is the column name and
                value is the column value
            where_stm (str): where clause
                
        """
        try:
            set_cmd = ""
            for k, v in col_val.items():
                set_cmd = '''"%s" = %s ''' % (k, v)
            cmd = '''UPDATE %s SET %s WHERE %s;''' % (
                self.get_tableName(), set_cmd, where_stm
            )
            self.execute_statement(cmd)            
        except Exception as e:
            if raise_I:
                raise
            else: 
                print(e)

    def delete_rows(self, where_stm, raise_I=False):
        """Delete table rows
        
        Args:
            where (str): where clause
        """
        try:
            cmd = '''DELETE FROM %s WHERE %s''' % (
                self.get_tableName(), where_stm
            )
            self.execute_statement(cmd)            
        except Exception as e:
            if raise_I:
                raise
            else: 
                print(e)

    def select_rows(
        self, 
        select_stm="*",
        where_stm="",
        group_by_stm="",
        having_stm="",
        order_by_stm="",
        limit_stm="",
        offset_stm="",
        raise_I=False
    ):
        """Select table rows
        """
        data_O = None
        try:
            cmd = '''SELECT %s FROM %s ''' % (select_stm, self.get_tableName())
            if where_stm:
                cmd += '''WHERE %s ''' % (where_stm)
            if group_by_stm:
                cmd += '''GROUP BY %s ''' % (group_by_stm)
            if having_stm:
                cmd += '''HAVING %s ''' % (having_stm)
            if order_by_stm:
                cmd += '''ORDER BY %s ''' % (order_by_stm)
            if limit_stm:
                cmd += '''LIMIT %s ''' % (limit_stm)
            if offset_stm:
                cmd += '''OFFSET %s ''' % (offset_stm)
            cmd = cmd[-1]
            cmd += ";"
            data_O = self.execute_select(cmd)            
        except Exception as e:
            if raise_I:
                raise
            else: 
                print(e)
        return data_O
