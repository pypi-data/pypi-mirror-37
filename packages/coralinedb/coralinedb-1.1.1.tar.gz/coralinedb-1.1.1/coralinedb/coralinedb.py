"""
    Coraline DB Manager - This will take care of reading and saving tables to SQL database
"""

# import python packages
import pandas as pd


class BaseDB:
    """
    Base class for all DB
    These functions must be inherited by sub-class
        - create_connection
        - show_databases
        - show_tables
    """
    def __init__(self, host, username, passwd):
        """
        Initial object by specify host username and password for database connection
        :param host: host name of the database (str)
        :param username: username of the database (str)
        :param passwd: password of the database (str)
        """
        self.host = host
        self.username = username
        self.passwd = passwd

    def create_connection(self, db_name=None):
        """
        Create Connection and engine for database
        :param: db_name : name of connecting database (str)
        :return: engine and connection
        """
        pass

    def load_table(self, db_name, table_name):
        """
        Load a table from database
        *The whole table will be download, please make sure you have enough memory*
        :param db_name: name of database (str)
        :param table_name: table name to be read (str)
        :return: pandas dataframe if table exists. Otherwise, None
        """

        # Create Connection
        engine, connection = self.create_connection(db_name)

        # Check if table exists and read
        if engine.dialect.has_table(engine, table_name):
            sql = 'SELECT * FROM %s' % table_name
            return pd.read_sql(sql, connection, coerce_float=False)
        else:
            print(table_name, "does not exist")
            return None

    def load_tables(self, db_name, table_names):
        """
        Load all tables from database
        *The whole table will be download, please make sure you have enough memory*
        :param db_name: name of database (str)
        :param table_names: list of table names (list of strings)
        :return: list of pandas dataframes if the corresponding table exists. Otherwise, None
        """
        # Create Connection
        engine, connection = self.create_connection(db_name)

        dfs = []

        # Load each table
        for tbn in table_names:
            if engine.dialect.has_table(engine, tbn):
                df = pd.read_sql('SELECT * FROM %s' % tbn, connection, coerce_float=False)
            else:
                print(tbn, "does not exist")
                df = None
            dfs.append(df)

        return dfs

    def save_table(self, df, db_name, table_name, if_exists='replace'):
        """
        Save pandas dataframe to database
        :param df: dataframe to be save (pandas dataframe)
        :param db_name: name of database (str)
        :param table_name: name of table (str)
        :param  if_exists: {'fail', 'replace', 'append'}, default 'replace'
            - fail: If table exists, do nothing.
            - replace: If table exists, drop it, recreate it, and insert data.
            - append: If table exists, insert data. Create if does not exist.
        :return:
        """

        # Create Connection
        engine, connection = self.create_connection(db_name)

        # Write stock_df to table tmp_status (if tmp_status exists, replace it)
        df.to_sql(name=table_name, con=engine, if_exists=if_exists, index=False)

    def show_databases(self):
        """
        list of all accessable databases on this host
        :return: list of database names
        """
        pass

    def show_tables(self, db_name):
        """
        List all tables in database
        :param db_name:  database name (str)
        :return: list of table names
        """
        pass

    def query(self, sql_statement, db_name=None):
        """
        Run SQL query
        :param sql_statement: SQL statement (str)
        :param db_name: database name
        :return:
        """
        # Create Connection
        engine, connection = self.create_connection(db_name)
        return pd.read_sql(sql_statement, connection, coerce_float=False)

    def get_count(self, db_name, table_name):
        """
        Get number of rows of a table
        :param db_name: database name (str)
        :param table_name: table name (str)
        :return:
        """
        # Create Connection
        engine, connection = self.create_connection(db_name)

        if engine.dialect.has_table(engine, table_name):
            sql = 'select count(*) from %s;' % table_name
            return pd.read_sql(sql, connection, coerce_float=False).iloc[:, 0].values[0]
        else:
            return None


def print_help():
    """
    print help
    :return:
    """
    print("Please go to https://pypi.org/project/coralinedb/ to see how to use the package")

