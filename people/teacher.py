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

    def add_teacher(self):
        """
        Adds new teacher to school.
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
            Teacher.DB.execute_query(query=query, params=values)
            Teacher.DB.commit()
        except:
            print("Failed to add teacher")

    @classmethod
    def remove_person(cls, person_code):
        """
        Removes a teacher record from database.
        If the selected teacher is enrolled in a class, the class record and
        all related class records will be removed from database.

        :param person_code: A unique code to remove teacher.
        """

        remove_query = """
        DELETE FROM teachers WHERE teacher_code = (%s)
        """

        try:
            cls.DB.execute_query(query=remove_query, params=(person_code,))
            cls.DB.commit()
            print(f"Teacher with code {person_code} removed!")
        except:
            print("Failed to remove teacher")
