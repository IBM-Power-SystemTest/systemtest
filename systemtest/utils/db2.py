"""
To handle the IBM_DB module simply and efficiently
"""

from typing import Any, Iterator
from pathlib import Path
import re

import ibm_db


class Database:
    """
    Gets an handle IBM BD2 connection and use a most common used
        References:
            https://github.com/ibmdb/python-ibmdb/wiki/APIs

    Attributes:
        config:
            Dictionary with the connection values, which will be
            transformed into the connection string.
        conn_str:
            String with the format needed to connect with IBM DB2
        conn:
            ibm_db conn
    """

    def __init__(self, database: str, user: str, password: str, host: str = "localhost", port: str = "50000", protocol: str = "TCPIP", *args, **kwargs):
        """
        Inits Database creating the config dict and connection string
        the connection is created only when necessary, such as fetching
        data

        Args:
            database:
                Database name
            user:
                Database user name
            password:
                Database password
            host:
                Optional; Host or IP where the database is
            port:
                Optional; Host port to get database access
            protocol:
                Optional; Protocol to connect with database, most common
                is TCPIP
            args:
                Optional; Ignore positional args
            kwargs:
                Optional; Ignore keyword args

        Returns:
            Database instance
        """

        self.config = {
            "DATABASE": database,
            "HOSTNAME": host,
            "PORT": port,
            "PROTOCOL": protocol,
            "UID": user,
            "PWD": password,
        }
        self.conn_str = self.get_conn_str(self.config)
        self.conn = None

    @staticmethod
    def get_conn_str(config_dict: dict[str, str]) -> str:
        """
        Parse a connection string based on a configuration dictionary
        Basically it concatenates key and value into a single string
        separated by ;.

        Args:
            config_dict:
                Dict with necesary config to create a connection string

        Returns:
            String with all values from the config dict

            example:
                'DATABASE=db_name;HOSTNAME=localhost;PORT=50000;PROTOCOL=TCPIP;UID=user_name;PWD=passw0rd'
        """
        conn_str = ";".join(
            (f"{key}={value}" for key, value in config_dict.items()))
        return conn_str

    def get_connection(self):
        """
        Uses the connection string to try to connect to the database.

        Args:
            Database instance

        Returns:
            If the connection is successful, the connection returns,
            otherwise it returns None printing the error message and code
        """
        try:
            conn = ibm_db.connect(self.conn_str, "", "")
            return conn
        except:
            error_code = ibm_db.conn_error()
            error_message = ibm_db.conn_errormsg()
            print(f"[{error_code}] Error in connection, sqlstate \n{error_message}")
            return None

    def close(self) -> bool:
        """
        Close the active connection of the instance,
        using the ibm_db.close.

        Args:
            Database instance

        Returns:
            Always returns a boolean, in case the connection is closed
            successfully or is already closed it returns True,
            in case of failure prints the error and returns False
        """
        if ibm_db.active(self.conn):
            try:
                closed = ibm_db.close(self.conn)
                print("Connection closed successfully")
            except Exception as error:
                print(error)
            finally:
                return closed
        else:
            print("Connection already closed")
            return True

    @staticmethod
    def get_sql(path: str, spaceless: bool = True) -> str:
        """
        Gets a sql query from a file and optionally removes unnecessary
        spaces.

        Args:
            path:
                Path to the file that contains the query, it will be
                converted to a Path object
            spaceless:
                Optional; If removes the additional spaces like \\n

        Returns:
            String with the static SQL query

            examples:
                'SELECT * FROM MY_TABLE'
        """
        sql_path = Path(path)
        with open(sql_path, "r") as sql_file:
            sql = sql_file.read()

        if spaceless:
            sql = re.sub(r"\s+", " ", sql)

        return sql

    def validate_conn(function):
        """
        Decorator to add to the methods that need to validate that it
        still has a connection but it does not have it reconnected
        """
        def wrapper(*args):
            # Gets the Database instance
            self = args[0]

            # Validating that the connection is still alive
            if ibm_db.active(self.conn):
                # If it has a connection, raise the function to the wrapper
                return function(*args)

            # Else reconnect and raise the function to the wrapper
            self.conn = self.get_connection()
            return function(*args)
        return wrapper

    @validate_conn
    def fetch(self, sql: str, transaction_unique: bool = True) -> Iterator[dict[str, Any]]:
        """
        Gets the rows of a query in the form of a generator of
        dictionaries, the dictionary keys are the column names.
        Using the ibm_db.fetch_assoc

        Args:
            self:
                Database intance
            sql:
                Query to perform
            transaction_unique:
                Optional; If the connection is going to be closed after
                executing the query

        Returns:
            Genetaror for each row fetched from the database

            example:
                [{
                    'name': 'Alan',
                    'last_name': 'Vazquez'
                },
                {
                    'name': 'Isaac',
                    last_name: None
                }]

            Casting the generator to a list gets each row as a dictionary
            with the column names as keys
        """
        # Executing query
        result = ibm_db.exec_immediate(self.conn, sql)
        # Fetching first row
        row = ibm_db.fetch_assoc(result)
        while (row):
            # Return row
            yield row
            # Getting the next row, until there is no more (row = None)
            row = ibm_db.fetch_assoc(result)

        # Close the connection if transaction is unique
        if transaction_unique:
            self.close()
