import re


class AccountManager:
    """
    A class responsible for managing user accounts and authentication.

    Attributes:
        database: A MySQLConnector object connected to the school database.
    """

    def __init__(self, database):
        """
        Initializes AccountManager object with given database.

        :param database: A MySQLConnector object which is connected to school database.
        """
        self.database = database

    def is_registered(self, person, person_code):
        """
        Checks if the person is already registered in the system.

        :param person: An object representing the person (e.g., Student or Teacher or Admin).
        :param person_code: The unique identifier (code) of the person.

        :return: True if the person is registered, False otherwise.
        """

        # Finding class of given person
        person_type = type(person).__name__.lower()

        # Searching through given person class table
        search_query = f"""
        SELECT * FROM {person_type + "s"}
        WHERE email = %s OR {person_type}_code = %s
        """

        try:
            # Get data from database
            result = self.database.execute_query(query=search_query, params=(person.email, person_code))
            return result
        except Exception as e:
            print("Something went wrong while checking registering...")
            return False

    def can_login(self, person, email, password):
        """
        Checks if the person can log in with the provided credentials.

        :param person: Type of person (e.g., Student or Teacher or Admin)
        :param email: A unique email for each person.
        :param password: password for given email.

        :return: True if login is successful, False otherwise.
        """

        # Searching for person through given table by email and password
        search_query = f"""
        SELECT * FROM {person + "s"}
        WHERE email = %s AND password = %s
        """

        try:
            result = self.database.execute_query(query=search_query, params=(email, password))
            return result
        except Exception as e:
            print("Something went wrong while login in...")
            return False

    @staticmethod
    def is_valid_email(email):
        """
        Validates the format of an email address.

        :param email: The email address to be validated.
        :return: True if the email address is valid, False otherwise.
        """

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if re.match(email_pattern, email):
            return True
        else:
            return False

    @staticmethod
    def is_valid_password(password):
        """
        Validates the format of a password.

        :param password: The password to be validated.
        :return: True if the password is valid, False otherwise.
        """

        if len(password) < 8:
            return False

        if not any(char.isdigit() for char in password):
            return False

        if not any(char.isalpha() for char in password):
            return False

        return True
