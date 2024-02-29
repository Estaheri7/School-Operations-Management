from people.person import *


class Admin(Person):
    def __init__(self, name, email, password, gender):
        """
        Initializes the Admin object with the provided parameters.

        :param name: Name of the admin,
        :param email: Unique email address.
        :param password: Password for admin.
        :param gender: Gender of new admin.
        """
        super().__init__(name, email, password, gender)

    def add_admin(self):
        """
        Adds new admin to school.

        :raise Exception: If admin cannot be added.
        """
        
        add_query = """
        INSERT INTO admins(name, email, password, gender)
        VALUES (%s, %s, %s, %s)
        """

        values = (
            self.name,
            self.email,
            self.password,
            self.gender
        )
        try:
            Admin.DB.execute_query(query=add_query, params=values)
            Admin.DB.commit()
        except Exception as e:
            raise e
