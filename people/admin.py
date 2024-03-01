from people.person import *
from people.student import Student
from people.teacher import Teacher


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

    @classmethod
    def do_object(cls, obj):
        """
        Perform actions related to different objects (students, teachers, etc.) based on the provided object type.

        :param obj: The type of object on which actions are to be performed (e.g., "student", "teacher").

        Prompts the user to specify an action (add, remove, update) to perform on the specified object type.
        Depending on the object type and action chosen:
        - Calls the corresponding static method to perform the action.
        - For example, if the object type is "student" and the action is "add", it calls the do_student method
          to add a new student.

        Valid object types:
        - "student": Perform actions related to students.
        - "teacher": Perform actions related to teachers.
        - "classroom": Perform actions related to classrooms.
        - "course": Perform actions related to courses.
        """
        
        method = input("Add/Remove/Update -> ").lower()
        if obj == "student":
            cls.do_student(method)
        elif obj == "teacher":
            cls.do_teacher(method)
        elif obj == "classroom":
            cls.do_classroom(method)
        elif obj == "course":
            cls.do_course(method)
        else:
            print("Invalid object!")

    @staticmethod
    def do_student(method):
        """
        Perform actions related to students based on the provided method.

        :param method: The action to perform on students (add, remove, update).

        For the 'add' method:
        - Prompts the user to enter data for new students either through input or by providing a CSV file path.
        - Calls the Student.get_attrs method to create Student objects from the entered data.
        - Adds each student to the database using the add_student method.

        For the 'remove' method:
        - Prompts the user to enter the student code to remove a student.
        - Calls the Student.remove_person method to remove the student from the database.

        For the 'update' method:
        - Prompts the user to enter the student code and new name/password to update student records.
        - Calls the Student.update_student method to update the student's name/password in the database.
        """

        if method == "add":
            file = input("Enter data through input (press enter) or write a csv file path: ")
            if not file.strip():
                file = None
            students = Student.get_attrs(file)
            for student in students:
                student.add_student()
        elif method == "remove":
            student_code = input("Enter student code to remove student: ")
            Student.remove_person(student_code)
        elif method == "update":
            student_code = int(input("Enter student code to update records: "))
            new_name = input("Enter new name: ")
            new_password = input("Enter new password: ")
            Student.update_student(student_code, (new_name, new_password))
        else:
            print("Invalid method")

    @staticmethod
    def do_teacher(method):
        """
        Perform actions related to teachers based on the provided method.

        :param method: The action to perform on teachers (add, remove, update).

        For the 'add' method:
        - Prompts the user to enter data for new teachers either through input or by providing a CSV file path.
        - Calls the Teacher.get_attrs method to create Teacher objects from the entered data.
        - Adds each teacher to the database using the add_teacher method.

        For the 'remove' method:
        - Prompts the user to enter the teacher code to remove a teacher.
        - Calls the Teacher.remove_person method to remove the teacher from the database.

        For the 'update' method:
        - Prompts the user to enter the teacher code, new name/password, and new department ID to update teacher records.
        - Calls the Teacher.update_teacher method to update the teacher's name/password/department in the database.
        """
        if method == "add":
            file = input("Enter data through input (press enter) or write a csv file path: ")
            if not file.strip():
                file = None
            teachers = Teacher.get_attrs(file)
            for teacher in teachers:
                teacher.add_teacher()
        elif method == "remove":
            teacher_code = input("Enter teacher code to remove teacher: ")
            Teacher.remove_person(teacher_code)
        elif method == "update":
            teacher_code = int(input("Enter teacher code to update records: "))
            new_name = input("Enter new name: ")
            new_password = input("Enter new password: ")
            new_department = int(input("Enter new department ID: "))
            Teacher.update_teacher(teacher_code, (new_name, new_password, new_department))
        else:
            print("Invalid method")

    @staticmethod
    def do_classroom(method):
        pass

    @staticmethod
    def do_course(method):
        pass

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

    @staticmethod
    def help():
        print("Welcome!\n")
        print("1 -> Add/Remove/Update student")
        print("2 -> Add/Remove/Update teacher")
        print("3 -> Add/Remove/Update classroom")
        print("4 -> Add/Remove/Update course")
        print("0 -> logout")
