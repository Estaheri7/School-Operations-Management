import mysql.connector
from mysql.connector import Error


class MySQLConnector:
    # Connecting to MySQL or Database if not None
    def __init__(self, host, user, password, db_name=None):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.db = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                databases=self.db_name
            )
            self.cursor = self.db.cursor()
        except Error as e:
            print(e)

    