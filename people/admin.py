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

    @staticmethod
    def enter_attrs():
        """
        Prompt the user to enter attributes for creating a new Admin object.

        :return: A tuple containing the entered attributes in the following order: (name, email, password, gender,
                 admin_code). If gender is not provided (blank input), it will be returned as None.
        """
        name = input("Enter name: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        gender = input("Enter your gender or blank: ")
        if not gender.strip():
            gender = None
        admin_code = input("Enter your unique code: ")
        return name, email, password, gender, admin_code
