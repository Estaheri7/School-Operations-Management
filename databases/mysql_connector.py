import mysql.connector
from mysql.connector import Error


class MySQLConnector:
    def __init__(self, host, user, password, db_name=None):
        """
        Initializes the MySQLConnector object with the provided parameters and
        establishes a connection to the MySQL server.

        :param host: The hostname or IP address of the MySQL server.
        :param user: The username for authentication.
        :param password: The password for authentication.
        :param db_name: The name of the database to connect to. If not provided,
                        connects to the MySQL server without selecting any database.
        """
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.db = None
        self.cursor = None
        self.connect()

    def connect(self):
        """
        Establishes a connection to the MySQL server using the provided credentials.

        :raises Error: if connection fails.
        """
        try:
            self.db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.db_name
            )
            self.cursor = self.db.cursor()
        except Error as e:
            print(e)

    def create_database(self, name):
        """
        Creates a new database with the given name if it does not already exist.

        :param name: A valid MySQL table creation query.
        :raises Error: if the database creation query execution fails.
        """
        try:
            query = f"CREATE DATABASE IF NOT EXISTS {name}"

            self.cursor.execute(query)
            self.db.database = name
            self.db_name = name
        except Error as e:
            print(e)

    def create_table(self, query):
        """
        Creates a table in the currently selected database using the provided SQL query.

        :param query: A MySQL table query.
        :raises Error: If table creation query execution fails.
        """
        try:
            self.cursor.execute(query)
        except Error as e:
            print(e)

    def execute_query(self, query, params=None):
        """
        Executes the given query with optional parameters.

        :param query: A valid MySQL query.
        :param params: Optional parameters to be used with the query, or None by default.
        :return: If the query is a SELECT query and returns results, returns a list of fetched rows.
                 Otherwise, returns None.
        """
        try:
            self.cursor.execute(query, params or ())
            if self.cursor.with_rows:
                return self.cursor.fetchall()
        except Error as e:
            print(e)

    def commit(self):
        """
        Commits the current transaction to the database.

        This method should be called after executing one or more SQL statements to permanently save the changes
        made during the transaction.
        """
        self.db.commit()

    def close(self):
        """
        Closes the connection to the MySQL server.

        This method should be called when you are done with the connection to free up any resources
        associated with the connection.
        """
        self.db.close()
