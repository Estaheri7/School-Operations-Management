from people.person import *
from account_management import AccountManager
from education import Classroom
import pandas as pd


class Teacher(Person):
    """
    Represents a teacher within the school system.

    Inherits from the Person class and provides additional functionality related to teacher operations
    such as adding, removing, or updating teacher records, adding grades for students in classes,
    searching for students enrolled in specific classes, and retrieving teacher attributes for creating Teacher objects.
    """

    def __init__(self, name, email, password, gender, teacher_code, department_id):
        """
        Initializes the Teacher object with the provided parameters.

        :param name: Name of the teacher.
        :param email: A unique email address for each teacher.
        :param password: Password for email address.
        :param gender: Gender of added teacher.
        :param teacher_code: A unique code for each teacher.
        :param department_id: An ID for teacher department.
        """
        super().__init__(name, email, password, gender)
        self.teacher_code = teacher_code
        self.department_id = department_id

    def add_teacher(self):
        """
        Adds new teacher to school.

        :raise Exception: If teacher cannot be added.
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
            Person.DB.execute_query(query=query, params=values)
            Person.DB.commit()
            print("Teacher added successfully!")
        except Exception as e:
            Person.logger.log(f"Error while adding teacher: {e}")

    @staticmethod
    def remove_person(person_code):
        """
        Removes a teacher record from database.
        If the selected teacher is enrolled in a class, the class record and
        all related class records will be removed from database.

        :param person_code: A unique code to remove teacher.
        """

        # Searching for teacher...
        result = Teacher.search_by_code(person_code)
        if not result:
            print("Teacher not found!")
            return

        remove_query = """
        DELETE FROM teachers WHERE teacher_code = (%s)
        """

        try:
            Person.DB.execute_query(query=remove_query, params=(person_code,))
            Person.DB.commit()
            print(f"Teacher with code {person_code} removed!")
        except Exception as e:
            Person.logger.log(f"Error while removing teacher: {e}")
            print("Failed to remove teacher")

    @staticmethod
    def update_teacher(teacher_code, new_values):
        """
        Updates records for teacher by given parameters.

        :param teacher_code: The teacher code identifying the teacher to be updated.
        :param new_values: A tuple containing the new values for the teacher attributes
                           in the following order: (name, password, department_id).
        """

        # Searching for teacher...
        result = Teacher.search_by_code(teacher_code)
        if not result:
            print("Teacher not found!")
            return

        update_query = f"""
        UPDATE teachers
        SET name = %s, password = %s, department_id = %s
        WHERE teacher_code = {teacher_code}
        """

        try:
            Person.DB.execute_query(query=update_query, params=new_values)
            Person.DB.commit()
            print(f"Records updated for teacher with code {teacher_code}")
        except Exception as e:
            Person.logger.log(f"Error while updating teacher: {e}")
            print("Failed to update records")

    def add_grade(self, student_code, class_code, new_grade):
        """
        Adds a grade for a student enrolled in a class.

        :param student_code: The unique code identifying the student.
        :param class_code: The unique code identifying the class.
        :param new_grade: The new grade to be added for the student in the class.

        Retrieves the class details using the provided class code. If the class is not found or the teacher
        does not teach the class, an error message is printed, and the method returns.

        Checks if the provided student is enrolled in the class. If enrolled, updates the grade for the student
        in the class by executing an SQL query. If successful, commits the transaction and prints a success message.
        If an error occurs during the update process, prints a failure message.
        """

        result = Classroom.search_by_code(class_code)
        if not result:
            print("Classroom not found!")
            return

        if self.teacher_code != result[0][5]:
            print("You don't own this classroom!")
            return

        enrolled = Teacher.find_student_class(student_code, class_code)
        if enrolled:
            update_query = f"""
            UPDATE student_classes
            SET grade = {new_grade}
            WHERE student_code = {student_code} AND class_code = {class_code}
            """
            try:
                Person.DB.execute_query(query=update_query)
                Person.DB.commit()
                print("grade added successfully!")
            except Exception as e:
                Person.logger.log(f"Error while adding grade: {e}")
                print("Failed to add grade!")
        else:
            print("Enrollment not found!")

    @staticmethod
    def find_student_class(student_code, class_code):
        """
        Searches for a student's enrollment record in a specific class.

        :param student_code: The unique code identifying the student.
        :param class_code: The unique code identifying the class.

        :return: A list of tuples containing the enrollment record if found, otherwise None.

        Executes an SQL query to search for a record in the student_classes table corresponding to the provided
        student code and class code. Returns the result of the query if a record is found, otherwise returns None.
        """

        search_query = """
        SELECT * FROM student_classes
        WHERE student_code = %s AND class_code = %s
        """
        try:
            result = Person.DB.execute_query(query=search_query, params=(student_code, class_code))
            return result
        except Exception as e:
            Person.logger.log(f"Error while searching for student classes: {e}")

    @staticmethod
    def search_by_code(teacher_code):
        search_query = f"""
        SELECT * FROM teachers
        WHERE teacher_code = {teacher_code}
        """

        return Person.DB.execute_query(query=search_query)

    @staticmethod
    def get_attrs(file=None):
        """
        Retrieve attributes for creating Teacher objects.

        :param file: Optional. Path to a CSV file containing teacher data. If provided,
                     attributes will be retrieved from the CSV file. If not provided,
                     attributes will be prompted from user input.
        :return: A list of Teacher objects initialized with the retrieved attributes.

        If 'file' is provided:
        - Reads the CSV file and extracts teacher attributes from it.
        - Converts 'teacher_code' and 'department_id' columns to integers.
        - Initializes Teacher objects with the retrieved attributes and adds them to a list.
        - Returns the list of Teacher objects.

        If 'file' is not provided:
        - Prompts the user to enter attributes for creating a new Teacher object.
        - If 'gender' is not provided (blank input), it will be set to None.
        - Converts 'teacher_code' and 'department_id' entered by the user to integers.
        - Initializes a new Teacher object with the entered attributes and returns it as a single-element list.
        """

        if file:
            try:
                # read teachers from csv file
                teachers = pd.read_csv(file)
                # declare empty list
                all_teachers = []
                # convert numpy int to mysql int
                teachers["teacher_code"] = teachers["teacher_code"].astype(int)
                teachers["department_id"] = teachers["department_id"].astype(int)
                for _, teacher_data in teachers.iterrows():
                    # checking if email is valid
                    if not AccountManager.is_valid_email(teacher_data["email"]):
                        print(f"Invalid email format for {teacher_data['email']}\nSkipped...")
                        continue
                    # checking if password is valid
                    if not AccountManager.is_valid_password(teacher_data["password"]):
                        print(f"Invalid password format for {teacher_data['email']}\nSkipped...")
                        continue
                    # create new teacher
                    new_teacher = Teacher(
                        teacher_data["name"],
                        teacher_data["email"],
                        teacher_data["password"],
                        teacher_data["gender"],
                        teacher_data["teacher_code"],
                        teacher_data["department_id"]
                    )
                    # add created object to created list
                    all_teachers.append(new_teacher)
                return all_teachers
            except FileNotFoundError as e:
                Person.logger.log(f"CSV file not found: {e}")
                print("File not found!")

        name = input("Enter name: ")
        email = input("Enter email: ")
        # checking if email is valid
        while not AccountManager.is_valid_email(email):
            email = input("Invalid email format! try another: ")
        password = input("Enter password: ")
        # checking is password is valid
        while not AccountManager.is_valid_password(password):
            print("1 - Password should be at least 9 characters")
            print("2 - Password should have number and alphabet too")
            password = input("Enter password: ")
        gender = input("Enter gender or enter to skip: ")
        if not gender.strip():
            gender = None
        teacher_code = input("Enter teacher code: ")
        department_id = input("Enter department ID: ")
        teacher = Teacher(name, email, password, gender, teacher_code, department_id)
        return [teacher]

    @staticmethod
    def help():
        print("1 -> Add grade")
        print("2 -> Search through your students.")
        print("3 -> Show grade plot of my students")
        print("0 -> log out")
