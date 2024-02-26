from people.person import *


class Teacher(Person):
    def __init__(self, name, email, password, gender, teacher_code, department_id):
        """
        Initializes the Teacher object with the provided parameters.

        :param name: Name of the teacher.
        :param email: A unique email address for each teacher.
        :param password: Password for email address.
        :param gender: Gender of added teacher.
        :param teacher_code: A unique code for each teacher.
        :param department_id: A unique ID for each teacher department.
        """
        super().__init__(name, email, password, gender)
        self.teacher_code = teacher_code
        self.department_id = department_id

    def add_teacher(self, database):
        """
        Adds new teacher to school.

        :param database: A MySQLConnector object which is connected to database.
        """

        query = """
        INSERT INTO teachers(name, email, password, gender, teacher_code, department_id)
        VALUES (%s, %s, %s, %s, %s, %s);
        """

        values = (
            self.name,
            self.email,
            self.password,
            self.gender,
            self.teacher_code,
            self.department_id
        )
        try:
            database.execute_query(query=query, params=values)
            database.commit()
        except:
            print("Failed to add teacher")