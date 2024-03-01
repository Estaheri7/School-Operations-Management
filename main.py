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

    ac = AccountManager(database)

    login = False
    while True:
        role = input("Select your role (Student, Teacher, Admin) or -1 to exit: ").lower()
        if role == "-1":
            break

        pick = int(input("Enter 1 to register or 2 to login: "))

        if role == "student":
            pass
        elif role == "teacher":
            pass
        elif role == "admin":
            admin = None
            if pick == 1:
                name, email, password, gender, admin_code = Admin.enter_attrs()
                admin = Admin(name, email, password, gender, admin_code)
                if not ac.is_registered(admin, admin_code):
                    admin.add_admin()
                    login = True
                    print("Registered successfully!")
                else:
                    print("This account is already registered!")
            elif pick == 2:
                email = input("Enter your email: ")
                password = input("Enter your password: ")
                let_login = ac.can_login(role, email, password)
                if let_login:
                    login = True
                    name, gender, admin_code = let_login[0][1], let_login[0][4], let_login[0][5]
                    admin = Admin(name, email, password, gender, admin_code)
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
                    Admin.do_person("student")
                elif choice == 2:
                    pass
                elif choice == 3:
                    pass
                elif choice == 4:
                    pass
                else:
                    print("Invalid command!")
        else:
            print("Invalid command!")


if __name__ == '__main__':
    main()
