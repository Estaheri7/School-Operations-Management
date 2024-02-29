class AccountManager:
    def __init__(self, database):
        """
        Initializes AccountManager object with given database.

        :param database: A MySQLConnector object which is connected to school database.
        """
        self.database = database

    def is_registered(self, person, person_code):
        person_type = type(person).__name__.lower()
        search_query = f"""
        SELECT * FROM {person_type + "s"}
        WHERE email = %s OR {person_type}_code = %s
        """

        result = self.database.execute_query(query=search_query, params=(person.email, person_code))
        return result
