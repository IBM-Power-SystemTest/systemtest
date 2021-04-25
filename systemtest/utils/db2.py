from typing import Any, Iterator
from pathlib import Path
import re

import ibm_db


class Database:
    def __init__(self, database: str, user: str, password: str, host: str = "localhost", port: str = "50000", protocol: str = "TCPIP", *args, **kwargs) -> None:
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
        conn_str = ";".join(
            (f"{key}={value}" for key, value in config_dict.items()))
        return conn_str

    def get_connection(self):
        try:
            conn = ibm_db.connect(self.conn_str, "", "")
            return conn
        except:
            error_code = ibm_db.conn_error()
            error_message = ibm_db.conn_errormsg()
            print(f"[{error_code}] Error in connection, sqlstate \n{error_message}")
            return None

    def close(self) -> bool:
        if ibm_db.active(self.conn):
            try:
                closed = ibm_db.close(self.conn)
            except Exception as error:
                print(error)
            finally:
                return closed
        else:
            print("Connection already closed")
            return True

    @staticmethod
    def get_sql(path: str, spaceless: bool = True) -> str:
        sql_path = Path(path)
        with open(sql_path, "r") as sql_file:
            sql = sql_file.read()

        if spaceless:
            sql = re.sub(r"\s+", " ", sql)

        return sql

    def validate_conn(function):
        def wrapper(*args):
            self = args[0]

            if ibm_db.active(self.conn):
                return function(*args)

            self.conn = self.get_connection()
            return function(*args)
        return wrapper

    @validate_conn
    def fetch(self, sql: str, transaction_unique: bool = True) -> Iterator[dict[str, Any]]:
        result = ibm_db.exec_immediate(self.conn, sql)
        row = ibm_db.fetch_assoc(result)
        while (row):
            yield row
            row = ibm_db.fetch_assoc(result)

        if transaction_unique:
            self.close()
