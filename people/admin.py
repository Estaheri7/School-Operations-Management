from people.person import Person
from people.student import Student
from people.teacher import Teacher
from education import Classroom, Course
from account_management import AccountManager


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
            Person.DB.execute_query(query=add_query, params=values)
            Person.DB.commit()
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
            student_code = input("Enter student code to update records: ")
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
            teacher_code = input("Enter teacher code to update records: ")
            new_name = input("Enter new name: ")
            new_password = input("Enter new password: ")
            new_department = int(input("Enter new department ID: "))
            Teacher.update_teacher(teacher_code, (new_name, new_password, new_department))
        else:
            print("Invalid method")

    @staticmethod
    def do_classroom(method):
        """
        Perform actions related to classrooms based on the provided method.

        :param method: The action to perform on classrooms (add, remove, update).

        For the 'add' method:
        - Prompts the user to enter data for new classrooms either through input or by providing a CSV file path.
        - Calls the Classroom.get_attrs method to create Classroom objects from the entered data.
        - Adds each classroom to the database using the add_classroom method.

        For the 'remove' method:
        - Prompts the user to enter the classroom code to remove a classroom.
        - Calls the Classroom.remove_classroom method to remove the classroom from the database.

        For the 'update' method:
        - Prompts the user to enter the classroom code, new name, current enrollment, new course code,
          and new teacher code to update classroom records.
        - Calls the Classroom.update_classroom method to update the classroom's attributes in the database.
        """

        if method == "add":
            file = input("Enter data through input (press enter) or write a csv file path: ")
            if not file.strip():
                file = None
            classrooms = Classroom.get_attrs(file)
            for classroom in classrooms:
                classroom.add_classroom()
        elif method == "remove":
            class_code = input("Enter classroom code to remove classroom: ")
            Classroom.remove_classroom(class_code)
        elif method == "update":
            class_code = input("Enter classroom code to update records: ")
            new_name = input("Enter new name: ")
            current_enrollment = input("Enter current enrollment: ")
            new_course_code = input("Enter new course code: ")
            new_teacher_code = input("Enter new teacher code: ")
            Classroom.update_classroom(class_code, (new_name, current_enrollment,
                                                    new_course_code, new_teacher_code))
        else:
            print("Invalid method!")

    @staticmethod
    def do_course(method):
        """
        Perform actions related to courses based on the provided method.

        :param method: The action to perform on courses (add, remove, update).

        For the 'add' method:
        - Prompts the user to enter data for new courses either through input or by providing a CSV file path.
        - Calls the Course.get_attrs method to create Course objects from the entered data.
        - Adds each course to the database using the add_course method.

        For the 'remove' method:
        - Prompts the user to enter the course code to remove a course.
        - Calls the Course.remove_course method to remove the course from the database.

        For the 'update' method:
        - Prompts the user to enter the course code, new name, and new capacity to update course records.
        - Calls the Course.update_course method to update the course's attributes in the database.
        """

        if method == "add":
            file = input("Enter data through input (press enter) or write a csv file path: ")
            if not file.strip():
                file = None
            courses = Course.get_attrs(file)
            for course in courses:
                course.add_course()
        elif method == "remove":
            course_code = input("Enter course code to remove course: ")
            Course.remove_course(course_code)
        elif method == "update":
            course_code = input("Enter course code to update records: ")
            new_name = input("Enter new name: ")
            new_capacity = input("Enter new capacity: ")
            Course.update_course(course_code, (new_name, new_capacity))
        else:
            print("Invalid method!")

    @staticmethod
    def enter_attrs():
        """
        Prompt the user to enter attributes for creating a new Admin object.

        :return: A tuple containing the entered attributes in the following order: (name, email, password, gender,
                 admin_code). If gender is not provided (blank input), it will be returned as None.
        """

        name = input("Enter name: ")
        email = input("Enter your email: ")
        while not AccountManager.is_valid_email(email):
            email = input("Invalid email! try another: ")
        password = input("Enter your password: ")
        while not AccountManager.is_valid_password(password):
            print("1 - Password should be at least 8 characters")
            print("2 - Password should have number and alphabet too")
            password = input("Enter password: ")
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
        print("5 -> Advance search")
        print("6 -> Show teacher workload")
        print("0 -> logout")
