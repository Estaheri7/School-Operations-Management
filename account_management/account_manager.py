class AccountManager:
    def __init__(self, database):
        """
        Initializes AccountManager object with given database.

        :param database: A MySQLConnector object which is connected to school database.
        """
        self.database = database

    def is_registered(self, person, person_code):
        """
        Checks if the person is already registered in the system.

        :param person: An object representing the person (e.g., Student or Teacher).
        :param person_code: The unique identifier (code) of the person.

        :return: True if the person is registered, False otherwise.
        """

        person_type = type(person).__name__.lower()

        search_query = f"""
        SELECT * FROM {person_type + "s"}
        WHERE email = %s OR {person_type}_code = %s
        """

        result = self.database.execute_query(query=search_query, params=(person.email, person_code))
        return result

    def can_login(self, person):
        """
        Checks if the person can log in with the provided credentials.

        :param person: An object representing the person (e.g., Student or Teacher).

        :return: True if login is successful, False otherwise.
        """

        person_type = type(person).__name__.lower()

        search_query = f"""
        SELECT * FROM {person_type + "s"}
        WHERE email = %s AND password = %s
        """

        result = self.database.execute_query(query=search_query, params=(person.email, person.password))
        return result
