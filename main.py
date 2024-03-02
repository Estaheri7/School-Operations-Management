from databases import MySQLConnector, tables, create_database
from data.initialize_data import *
from people import Admin
from account_management import *


def main() -> None:
    database = create_database.db
    try:
        initialize_data(
            "data\\classrooms.json",
            "data\\courses.json",
            "data\\teachers.json",
            "data\\students.json",
            "data\\admins.json"
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
            if pick == 1:
                student = Student.get_attrs()
                if not AM.is_registered(student[0], student[0].student_code):
                    student[0].add_student()
                    login = True
                else:
                    print("This account is already registered!")
            elif pick == 2:
                email = input("Enter your email: ")
                password = input("Enter your password: ")
                if AM.can_login(role, email, password):
                    login = True
                    print("Logged in successfully")
                else:
                    print("Invalid email or password!")
            else:
                print("Invalid command!")
            while login:
                print("done")
                break
        elif role == "teacher":
            pass
        elif role == "admin":
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
