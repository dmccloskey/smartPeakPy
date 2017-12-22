# -*- coding: utf-8 -*-
from .DBio import DBio
import copy


class DBTableInterface(DBio):
    """DB table interface
    
    All DB table classes should inherit this object
    """
    def __init__(
        self, dialect, table_name, schema_name, 
        columns, data_types, constraint_names, constraints
    ):
        """Initialize all attributes
        
        Args:
            dialect (str): dialect e.g., postgresql, sqlite, etc.,
            table_name (str): name of the table
            schema_name (str): name of the schema that the table belongs
            columns (list): list of column names
            data_types (list): list of data types that match the list of column names
            constraint_names (list): list of constraint names
            constraints (list): list of sql text constraints
        """
        self.dialect_ = dialect
        self.table_name_ = table_name
        self.schema_name_ = schema_name
        self.columns_ = columns
        self.data_types_ = data_types
        assert(len(self.columns_) == len(self.data_types_))
        self.constraint_names_ = constraint_names
        self.constraints_ = constraints
        assert(len(self.constraint_names_) == len(self.constraints_))
        self.pcol_ = "id"
        self.timestamp_ = "date_and_time"

    def get_tableName(self):
        """Return a table name"""
        table_name = ""
        if self.schema_name_ is not None:
            table_name = '''"%s".''' % (self.schema_name_)
        table_name += '''"%s"''' % (self.table_name_)
        return table_name

    def get_tableColumns(self):
        """Return a list of table columns"""
        columns = copy.copy(self.columns_)
        columns.insert(0, self.timestamp_)
        columns.insert(0, self.pcol_)
        return columns

    def get_sequenceName(self):
        """Return the sequence name"""
        seq_name = '''"%s_%s_seq"''' % (self.table_name_, self.pcol_)
        return seq_name

    def create_table(self, raise_I=False):
        """Create a table"""
        try:
            if self.dialect_ == "postgresql":
                # make the sequence
                self.create_sequence(raise_I)

            # make the columns
            col_type_stmt = ""
            if self.dialect_ == "postgresql":
                col_type_stmt += '''%s INTEGER NOT NULL CONSTRAINT "%s_pkey" PRIMARY KEY DEFAULT nextval('%s'), 
                ''' % (self.pcol_, self.table_name_, self.get_sequenceName())
            elif self.dialect_ == "sqlite3":
                col_type_stmt += '''%s INTEGER NOT NULL CONSTRAINT "%s_pkey" PRIMARY KEY AUTOINCREMENT, 
                ''' % (self.pcol_, self.table_name_)
            col_type_stmt += '''%s TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, ''' % (
                self.timestamp_) 
            for i in range(len(self.columns_)):
                col_type_stmt += '''"%s" %s, ''' % (
                    self.columns_[i], 
                    self.data_types_[i]
                )
            col_type_stmt = col_type_stmt[:-2]

            # make the table constraints
            constraints_stmt = ", "
            for i in range(len(self.constraints_)):
                constraints_stmt += '''CONSTRAINT "%s" %s, ''' % (
                    self.constraint_names_[i], self.constraints_[i]
                )
            constraints_stmt = constraints_stmt[:-2]

            # make the table
            cmd = """CREATE TABLE IF NOT EXISTS %s (%s%s);""" % (
                self.get_tableName(), col_type_stmt, constraints_stmt)
            self.execute_statement(cmd, raise_I)

            if self.dialect_ == "postgresql":
                alter_stmt = '''ALTER SEQUENCE %s OWNED BY %s."%s";''' % (
                    self.get_sequenceName(), self.get_tableName, self.pcol_)
                self.execute_statement(alter_stmt, raise_I)                

        except Exception as e:
            if raise_I:
                raise
            else: 
                print(e)

    def drop_table(self, raise_I=False):
        """Drop a table"""
        try:
            if self.dialect_ == "postgresql":
                # drop the primar key constratin
                alter_stm = '''DROP CONSTRAINT IF EXISTS "%s_pkey"''' % (
                    self.table_name_)
                self.alter_table(alter_stm, raise_I)

                # drop the constraints
                for constraint_name in self.constraint_names_:
                    alter_stm = '''DROP CONSTRAINT IF EXISTS "%s"''' % (
                        constraint_name
                    )
                    self.alter_table(alter_stm, raise_I)

                # drop the sequence
                self.drop_sequence(raise_I)

            # drop the table
            cmd = """DROP TABLE IF EXISTS %s;""" % (
                self.get_tableName())
            self.execute_statement(cmd, raise_I)
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
            cmd = 'ALTER TABLE %s %s' % (
                self.get_tableName(), alter_stm)
            self.execute_statement(cmd, raise_I)
        except Exception as e:
            if raise_I:
                raise
            else: 
                print(e)

    def create_sequence(self, raise_I=False):
        """Create a sequence on a table"""
        try:
            cmd = '''CREATE SEQUENCE IF NOT EXISTS "%s_%s_seq" ON %s.%s;''' % (
                self.table_name_, self.pcol_, self.get_tableName(), self.pcol_
            )
            self.execute_statement(cmd, raise_I)
        except Exception as e:
            if raise_I:
                raise
            else: 
                print(e)

    def drop_sequence(self, raise_I=False):
        """Drop a sequence on a table"""
        
        try:
            cmd = '''DROP SEQUENCE IF NOT EXISTS "%s_%s_seq";''' % (
                self.table_name_, self.pcol_
            )
            self.execute_statement(cmd, raise_I)
        except Exception as e:
            if raise_I:
                raise
            else: 
                print(e)

    def create_trigger(
        self, trigger_name, before_after_insteadOf, 
        event, func_name, raise_I=False
    ):
        """Create a trigger on a table

        Args:
            ...
            func_name (str): name of the function (postgresql); procedure (sqlite)
        """
        try:
            if before_after_insteadOf not in ["BEFORE", "AFTER", "INSTEAD OF"]:
                raise NameError("Invalid option given for before_after_insteadOf \
                parameter.")
            if event not in ["INSERT", "UPDATE", "DELETE", "TRUNCATE"]:
                raise NameError("Invalid option given for even parameter.")
            if self.dialect_ == "postgresql":
                cmd = '''CREATE TRIGGER "%s" %s %s ON %s EXECUTE PROCEDURE "%s";''' % (
                    trigger_name, before_after_insteadOf, event, self.get_tableName(),
                    func_name
                )
            elif self.dialect_ == "sqlite3":
                cmd = '''CREATE TRIGGER "%s" %s %s ON %s BEGIN %s END;''' % (
                    trigger_name, before_after_insteadOf, event, self.get_tableName(),
                    func_name
                )
            self.execute_statement(cmd, raise_I)
        except Exception as e:
            if raise_I:
                raise
            else: 
                print(e)

    def drop_trigger(self, trigger_name, raise_I=False):
        """Drop a trigger"""        
        try:
            cmd = '''DROP TRIGGER IF EXISTS "%s";''' % (
                trigger_name)
            self.execute_statement(cmd, raise_I)
        except Exception as e:
            if raise_I:
                raise
            else: 
                print(e)

    # def create_function(
    #     self, func_name, argnames,
    #     return_type, raise_I=False
    # ):
    #     """Create function

    #     NOTE: not available in sqlite
        
    #     """
    #     try:
    #         args = ""
    #         cmd = '''CREATE OR REPLACE FUNCTION "%s" (%s) RETURNS %s AS $$ BEGIN %s END;\
    #         ''' % (
    #             func_name, args, return_type,
    #         )
    #         self.execute_statement(cmd, raise_I)
    #     except Exception as e:
    #         if raise_I:
    #             raise
    #         else: 
    #             print(e)

    # def drop_function(self, raise_I=False):
    #     """Drop function

    #     NOTE: not available in sqlite
        
    #     """
    #     pass

    def insert_row(self, col_val, raise_I=False):
        """insert a table row
        
        Args:
            col_val (dict): key, value pair where key is the column name and
                value is the column value
        
        """
        try:
            insert_cols = ""
            insert_vals = ""
            for k, v in col_val.items():
                insert_cols += '''"%s", ''' % (k)
                insert_vals += '''%s, ''' % (v)
            insert_cols = insert_cols[:-2]
            insert_vals = insert_vals[:-2]
            cmd = """INSERT INTO %s (%s) VALUES (%s);""" % (
                self.get_tableName(), insert_cols, insert_vals)
            self.execute_statement(cmd, raise_I)
        except Exception as e:
            if raise_I:
                raise
            else: 
                print(e)

    def insert_rows(self, rows, raise_I=False):
        """Insert table rows
        
        Args:
            rows (list): list of key, value pairs
        
        """
        try:
            for row in rows:
                self.insert_row(row)
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
                set_cmd += '''"%s" = %s ''' % (k, v)
            cmd = '''UPDATE %s SET %s WHERE %s;''' % (
                self.get_tableName(), set_cmd, where_stm
            )
            self.execute_statement(cmd, raise_I)            
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
            self.execute_statement(cmd, raise_I)            
        except Exception as e:
            if raise_I:
                raise
            else: 
                print(e)

    def select_rows(
        self, 
        select_list,
        where_stm="",
        group_by_stm="",
        having_stm="",
        order_by_stm="",
        limit_stm="",
        offset_stm="",
        raise_I=False
    ):
        """Select table rows

        Args:
            select_list (list): list of table columns to select
            where_stm (str): WHERE clause
            group_by_stm (str): GROUP BY clause
            having_stm (str): HAVING clause
            order_by_stm (str): ORDER BY clause
            limit_stm (str): LIMIT clause
            offset_stm (str): OFFSET clause
        """
        data_O = None
        try:
            cmd = '''SELECT %s FROM %s ''' % (
                self.convert_list2string(select_list), self.get_tableName())
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
            cmd = cmd[:-1]
            cmd += ";"
            data_O = self.execute_select(cmd, select_list, raise_I)            
        except Exception as e:
            if raise_I:
                raise
            else: 
                print(e)
        return data_O
