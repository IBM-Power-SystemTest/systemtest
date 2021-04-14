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
        self.conn = None

    @staticmethod
    def get_conn_str(config_dict: dict[str, str]) -> str:
        conn_str = ";".join(
            (f"{key}={value}" for key, value in config_dict.items()))
        return conn_str

    def connect(self):
        try:
            conn = ibm_db.connect(self.get_conn_str(self.config))
            return conn
        except:
            print("Error in connection, sqlstate = ")
            errorMsg = ibm_db.conn_errormsg()
            print(errorMsg)
            return None

    def get_connection(self):
        if self.conn is None:
            self.conn = self.connect()

        return self.conn

    def close(self):
        return ibm_db.close(self.conn)
