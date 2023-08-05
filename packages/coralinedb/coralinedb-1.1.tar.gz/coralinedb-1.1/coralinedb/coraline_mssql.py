from sqlalchemy import create_engine
import time
import pandas as pd
from coralinedb import BaseDB


class MSSQLDB(BaseDB):
    """
    Class for MS SQL Server
    """

    def create_connection(self, db_name=None):

        """
        Create Connection and engine for database
        :param: db_name : name of connecting database (str)
        :return: engine and connection
        """
        connected = False
        max_tries = 10

        # if db_name is not defined, let it be empty string
        if db_name is None:
            db_name = ""

        # Reconnect until max_tries exceeded
        while not connected and max_tries > 0:
            try:

                # create engine from db settings
                engine = create_engine("mssql+pymssql://" + self.username + ":" + self.passwd + '@' + self.host + '/' + db_name)

                # Create connection for query
                connection = engine.connect()

                connected = True

                return engine, connection
            except Exception as e:
                print("Database Connection Error: {}".format(e))
                print("Network is unreachable. Retrying to connect to database in 10 seconds...")
                time.sleep(10)
                max_tries -= 1

    def show_databases(self):
        """
        list of all accessable databases on this host
        :return: list of database names
        """
        # Create Connection
        engine, connection = self.create_connection()

        sql = 'SELECT name FROM master.sys.databases;'
        return pd.read_sql(sql, connection, coerce_float=False).iloc[:, 0].values

    def show_tables(self, db_name):
        """
        List all tables in database
        :param db_name:  database name (str)
        :return: list of table names
        """
        # Create Connection
        engine, connection = self.create_connection(db_name)

        sql = 'SELECT * FROM information_schema.tables;'
        return pd.read_sql(sql, connection, coerce_float=False)['TABLE_NAME'].values


