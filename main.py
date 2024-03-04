from databases import MySQLConnector, tables, create_database
from people import Admin, Student, Teacher
from education import Classroom, Course
from data.initialize_data import initialize_data
from account_management import *
from searcher import Searcher


def main() -> None:
    database = create_database.db
    try:
        initialize_data(
            r"data\classrooms.json",
            r"data\courses.json",
            r"data\teachers.json",
            r"data\students.json",
            r"data\admins.json"
        )
    except:
        pass

    AM = AccountManager(database)

    login = False
    while True:
        role = input("Select your role (Student, Teacher, Admin) or -1 to exit: ").lower()
        if role == "-1":
            break

        pick = int(input("Enter 1 to register or 2 to login: "))

        if role == "student":
            Student.DB = create_database.db
            current_student = None
            if pick == 1:
                student = Student.get_attrs()
                if not AM.is_registered(student[0], student[0].student_code):
                    student[0].add_student()
                    login = True
                    current_student = student[0]
                else:
                    print("This account is already registered!")
            elif pick == 2:
                email = input("Enter your email: ")
                password = input("Enter your password: ")
                let_login = AM.can_login(role, email, password)
                if let_login:
                    login = True
                    current_student = Student(
                        let_login[0][1],
                        let_login[0][2],
                        let_login[0][3],
                        let_login[0][4],
                        let_login[0][5]
                    )
                    print("Logged in successfully")
                else:
                    print("Invalid email or password!")
            else:
                print("Invalid command!")
            while login:
                Student.help()
                choice = int(input())
                if choice == 0:
                    login = False
                    break
                if choice == 1:
                    print("Classes to enroll: ")
                    Searcher.DB = create_database.db
                    Searcher.display_classroom(Searcher.advanced_search("classrooms"))
                    class_code = input("Enter class code: ")
                    current_student.enroll(class_code)
                elif choice == 2:
                    print("Your enrollments: ")
                    Searcher.DB = create_database.db
                    conditions = {"student_code": current_student.student_code}
                    Searcher.display_enrolled(Searcher.advanced_search("student_classes", conditions))
                    class_code = input("Enter class code: ")
                    current_student.delete_enrollment(class_code)
                else:
                    print("Invalid command!")
        elif role == "teacher":
            Teacher.DB = create_database.db
            current_teacher = None
            if pick == 1:
                teacher = Teacher.get_attrs()
                if not AM.is_registered(teacher[0], teacher[0].teacher_code):
                    teacher[0].add_teacher()
                    login = True
                    current_teacher = teacher[0]
                else:
                    print("This account is already registered!")
            elif pick == 2:
                email = input("Enter your email: ")
                password = input("Enter your password: ")
                let_login = AM.can_login(role, email, password)
                if let_login:
                    login = True
                    current_teacher = Teacher(
                        let_login[0][1],
                        let_login[0][2],
                        let_login[0][3],
                        let_login[0][4],
                        let_login[0][5],
                        let_login[0][6]
                    )
                    print("Logged in successfully")
                else:
                    print("Invalid email or password!")
            else:
                print("Invalid command!")
            while login:
                Teacher.help()
                choice = int(input())
                if choice == 0:
                    login = False
                    break
                if choice == 1:
                    student_code = input("Enter student code: ")
                    class_code = input("Enter class code: ")
                    new_grade = int(input("Enter grade: "))
                    current_teacher.add_grade(student_code, class_code, new_grade)
                else:
                    print("Invalid command!")
        elif role == "admin":
            Admin.DB = create_database.db
            if pick == 1:
                name, email, password, gender, admin_code = Admin.enter_attrs()
                admin = Admin(name, email, password, gender, admin_code)
                if not AM.is_registered(admin, admin_code):
                    admin.add_admin()
                    login = True
                    print("Registered successfully!")
                else:
                    print("This account is already registered!")
            elif pick == 2:
                email = input("Enter your email: ")
                password = input("Enter your password: ")
                let_login = AM.can_login(role, email, password)
                if let_login:
                    login = True
                    print("Logged in successfully!")
                else:
                    print("Invalid email or password!")
            else:
                print("Invalid command!")
            while login:
                Admin.help()
                choice = int(input())
                if choice == 0:
                    login = False
                    break
                elif choice == 1:
                    Admin.do_object("student")
                elif choice == 2:
                    Admin.do_object("teacher")
                elif choice == 3:
                    Admin.do_object("classroom")
                elif choice == 4:
                    Admin.do_object("course")
                else:
                    print("Invalid command!")
        else:
            print("Invalid command!")


if __name__ == '__main__':
    main()
