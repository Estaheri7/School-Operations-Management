from people.person import *
from education import Classroom, Course
from account_management import AccountManager
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

    @classmethod
    def update_student(cls, student_code, new_values):
        """
        Updates records for teacher by given parameters.

        :param student_code: The student code identifying the student to be updated.
        :param new_values: A tuple containing the new values for the student attributes
                           in the following order: (name, password).
        """

        update_query = f"""
        UPDATE students
        SET name = %s, password = %s
        WHERE student_code = {student_code}
        """

        try:
            cls.DB.execute_query(query=update_query, params=new_values)
            cls.DB.commit()
            print(f"Records updated for student with code {student_code}")
        except:
            print("Failed to update records")

    def enroll(self, class_code):
        """
        Enrolls the student in a class identified by the given class code.

        :param class_code: The unique code identifying the class to enroll in.

        Checks if the student is already enrolled in the specified class.
        If not enrolled, checks if there is available space in the class.
        If space is available, enrolls the student in the class and updates the enrollment count.
        Otherwise, displays a message indicating that the class is full or the student is already enrolled.
        """

        if self.is_enrolled(self.student_code, class_code):
            print("This student has already enrolled this class!")
            return

        classroom = Classroom.search_by_code(class_code)
        if not classroom:
            print("Classroom not found (Invalid class code)")
            return

        access, msg = self.change_enrollment_value("add", classroom)
        if access:
            enroll_query = """
            INSERT INTO student_classes(student_code, class_code)
            VALUES (%s, %s)
            """

            try:
                Student.DB.execute_query(query=enroll_query, params=(self.student_code, class_code))
                Student.DB.commit()
                print(msg)
            except:
                print("Failed to enroll class")
        else:
            print(msg)

    def delete_enrollment(self, class_code):
        """
        Removes the student's enrollment from the class identified by the given class code.

        :param class_code: The unique code identifying the class to remove enrollment from.

        Checks if the student is enrolled in the specified class.
        If enrolled, removes the student's enrollment from the class and updates the enrollment count.
        Otherwise, displays a message indicating that the student is not enrolled in the class.
        """
        
        if not self.is_enrolled(self.student_code, class_code):
            print("enrollment not found!")
            return

        classroom = Classroom.search_by_code(class_code)
        if not classroom:
            print("Classroom not found! (Invalid class code)")
            return

        access, msg = self.change_enrollment_value("delete", classroom)
        if access:
            delete_query = f"""
            DELETE FROM student_classes
            WHERE student_code = {self.student_code} AND class_code = {class_code} 
            """

            try:
                Student.DB.execute_query(query=delete_query)
                Student.DB.commit()
                print(msg)
            except:
                print("Failed to delete enrollment!")
        else:
            print(msg)

    @classmethod
    def is_enrolled(cls, student_code, class_code):
        """
        Check if a student with the given student code is enrolled in a class with the given class code.

        :param student_code: The unique code identifying the student.
        :param class_code: The unique code identifying the class.
        :return: True if the student is enrolled in the class, False otherwise.

        Executes a SQL query to check if there is a record in the student_classes table
        corresponding to the provided student code and class code. Returns True if such
        a record exists (indicating the student is enrolled in the class), and False otherwise.
        """

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
    def change_enrollment_value(method, classroom):
        """
        Modify the enrollment value for the given classroom.

        :param method: The method to perform, either 'add' to increment enrollment or 'delete' to decrement it.
        :param classroom: A tuple representing the classroom details retrieved from the database.

        :return: A tuple containing a boolean indicating if the operation was successful,
                 and a message indicating the result of the operation.

        If 'method' is 'add' and there is still capacity in the classroom:
        - Increases the current enrollment of the classroom by one.
        - Commits the changes to the database.

        If 'method' is 'delete' and the classroom has at least one enrollment:
        - Decreases the current enrollment of the classroom by one.
        - Commits the changes to the database.

        If 'method' is 'delete' and the classroom has no enrollments:
        - Returns False and a message indicating that the class has no enrollments.

        If 'method' is 'add' and the classroom is already at full capacity:
        - Returns False and a message indicating that the class is full.
        """

        course_code = classroom[0][4]
        current_enrollment = classroom[0][2]

        course = Course.search_by_code(course_code)
        capacity = course[0][3]

        if current_enrollment < capacity and method == "add":
            update_query = f"""
            UPDATE classrooms
            SET current_enrollment = current_enrollment + 1
            WHERE class_code = {classroom[0][3]}
            """

            Student.DB.execute_query(query=update_query)
            Student.DB.commit()
        elif current_enrollment > 0 and method == "delete":
            update_query = f"""
            UPDATE classrooms
            SET current_enrollment = current_enrollment - 1
            WHERE class_code = {classroom[0][3]}
            """

            Student.DB.execute_query(query=update_query)
            Student.DB.commit()
        elif current_enrollment == 0 and method == "delete":
            return False, "Selected class does not have enrollment at all!"
        else:
            return False, "Selected class is full!"
        return True, "Done!"

    @staticmethod
    def get_attrs(file=None):
        """
        Retrieve attributes for creating Student objects.

        :param file: Optional. Path to a CSV file containing student data. If provided,
                     attributes will be retrieved from the CSV file. If not provided,
                     attributes will be prompted from user input.
        :return: A list of Student objects initialized with the retrieved attributes.

        If 'file' is provided:
        - Reads the CSV file and extracts student attributes from it.
        - Converts 'student_code' column to integers.
        - Initializes Student objects with the retrieved attributes and adds them to a list.
        - Returns the list of Student objects.

        If 'file' is not provided:
        - Prompts the user to enter attributes for creating a new Student object.
        - If 'gender' is not provided (blank input), it will be set to None.
        - Converts 'student_code' entered by the user to an integer.
        - Initializes a new Student object with the entered attributes and returns it as a single-element list.
        """

        if file:
            all_students = []
            students = pd.read_csv(file)
            students["student_code"] = students["student_code"].astype(int)
            for _, student_data in students.iterrows():
                if not AccountManager.is_valid_email(student_data["email"]):
                    print(f"Invalid email format for {student_data['email']}\nSkipped...")
                    continue
                if not AccountManager.is_valid_password(student_data["password"]):
                    print(f"Invalid password format for {student_data['email']}\nSkipped...")
                    continue
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
        while not AccountManager.is_valid_email(email):
            email = input("Invalid email format! try another: ")
        password = input("Enter password: ")
        while not AccountManager.is_valid_password(password):
            print("1 - Password should be at least 8 characters")
            print("2 - Password should have number and alphabet too")
            password = input("Enter password: ")
        gender = input("Enter gender: ")
        if not gender.strip():
            gender = None
        student_code = input("Enter student code: ")
        student = Student(name, email, password, gender, student_code)
        return [student]

    @staticmethod
    def help():
        print("Welcome!\n")
        print("1 -> Enroll to class")
        print("2 -> Remove your enrollment from class")
        print("0 -> logout")
