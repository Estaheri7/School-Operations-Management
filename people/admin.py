from people.person import *


class Admin(Person):
    def __init__(self, name, email, password, gender, admin_code):
        """
        Initializes the Admin object with the provided parameters.

        :param name: Name of the admin,
        :param email: Unique email address.
        :param password: Password for admin.
        :param gender: Gender of new admin.
        :param admin_code: A unique code for each admin.
        """
        super().__init__(name, email, password, gender)
        self.admin_code = admin_code

    def add_admin(self):
        """
        Adds new admin to school.

        :raise Exception: If admin cannot be added.
        """
        
        add_query = """
        INSERT INTO admins(name, email, password, gender, admin_code)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            self.name,
            self.email,
            self.password,
            self.gender,
            self.admin_code
        )
        try:
            Admin.DB.execute_query(query=add_query, params=values)
            Admin.DB.commit()
            print("Admin added successfully!")
        except Exception as e:
            raise e
