from people.person import *
import pandas as pd


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

    def add_student(self):
        """
        Adds new student to school.

        :raise Exception: If student cannot be added.
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
            print("Student added successfully!")
        except Exception as e:
            raise e

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

        if self.is_enrolled(self.student_code, class_code):
            print("This student already enrolled this class!")
            return

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

    @classmethod
    def is_enrolled(cls, student_code, class_code):
        search_query = """
        SELECT student_class_id FROM student_classes
        WHERE student_code = %s AND class_code = %s
        """
        try:
            result = cls.DB.execute_query(query=search_query, params=(student_code, class_code))
            return result
        except:
            print("Something went wrong when enrolling.")
            return None

    @staticmethod
    def get_attrs(file=None):
        if file:
            all_students = []
            students = pd.read_csv(file)
            students["student_code"] = students["student_code"].astype(int)
            for _, student_data in students.iterrows():
                new_student = Student(
                    student_data["name"],
                    student_data["email"],
                    student_data["password"],
                    student_data["gender"],
                    student_data["student_code"]
                )
                all_students.append(new_student)
            return all_students

        name = input("Enter name: ")
        email = input("Enter email: ")
        password = input("Enter password: ")
        gender = input("Enter gender: ")
        if not gender.strip():
            gender = None
        student_code = input("Enter student code: ")
        student = Student(name, email, password, gender, student_code)
        return [student]
