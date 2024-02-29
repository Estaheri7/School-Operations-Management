class AccountManager:
    def __init__(self, database):
        """
        Initializes AccountManager object with given database.

        :param database: A MySQLConnector object which is connected to school database.
        """
        self.database = database

    