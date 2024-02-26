from people.person import *


class Student(Person):
    def __init__(self, name, email, password, gender, student_code):
        """
        Initializes the Student object with the provided parameters.

        :param name: Name of the student,
        :param email: Unique email address.
        :param password: Password for student.
        :param gender: Gender of new student.
        :param student_code: A unique code for each student.
        """
        super().__init__(name, email, password, gender)
        self.student_code = student_code

    def add_student(self, database):
        """
        Adds new student to school.

        :param database: A MySQLConnector object which is connected to database.
        """

        query = """
        INSERT INTO students(name, email, password, gender, student_code)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            self.name,
            self.email,
            self.password,
            self.gender,
            self.student_code
        )
        try:
            database.execute_query(query=query, params=values)
            database.commit()
        except:
            print("Failed to add student")
