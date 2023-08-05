# import python packages
import pandas as pd
from sqlalchemy import create_engine
import time
from coralinedb import BaseDB


class MySQLDB(BaseDB):
    """
    Class for MySQL Database
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
                engine = create_engine("mysql://" + self.username + ":" + self.passwd + '@' + self.host + '/' + db_name + '?charset=utf8mb4')

                # Create connection for query
                connection = engine.raw_connection()

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

        sql = 'show databases;'
        return pd.read_sql(sql, connection, coerce_float=False).iloc[:, 0].values

    def show_tables(self, db_name):
        """
        List all tables in database
        :param db_name:  database name (str)
        :return: list of table names
        """
        # Create Connection
        engine, connection = self.create_connection(db_name)

        sql = 'show tables;'
        return pd.read_sql(sql, connection, coerce_float=False).iloc[:, 0].values
