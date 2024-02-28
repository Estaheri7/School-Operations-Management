from people.person import *
from databases import MySQLConnector
import json


class Student(Person):
    with open("databases/db_info.json", "r") as file:
        db_info = json.load(file)
    DB = MySQLConnector(**db_info)

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

    def add_student(self):
        """
        Adds new student to school.
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
            Student.DB.execute_query(query=query, params=values)
            Student.DB.commit()
        except:
            print("Failed to add student")

    @classmethod
    def remove_person(cls, person_code):
        """
        Removes a student record from database.
        If a selected student is enrolled in a class, their record will be removed from
        the student_classes table.

        :param person_code: A unique code to remove student.
        """

        remove_query = """
        DELETE FROM students WHERE student_code = (%s)
        """

        try:
            cls.DB.execute_query(query=remove_query, params=(person_code,))
            cls.DB.commit()
            print(f"Student with code {person_code} removed!")
        except:
            print("Failed to remove Student")

    def enroll(self, class_code):
        """
        Enrolls a class for given student_code.

        :param class_code:  given class for enroll.
        """

        enroll_query = """
        INSERT INTO student_classes(student_code, class_code)
        VALUES (%s, %s)
        """

        try:
            Student.DB.execute_query(query=enroll_query, params=(self.student_code, class_code))
            Student.DB.commit()
            print("Enrolled to class successfully!")
        except:
            print("Failed to enroll class")
    