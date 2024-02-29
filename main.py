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
            if pick == 1:
                name, email, password, gender, admin_code = Admin.enter_attrs()
                admin = Admin(name, email, password, gender, admin_code)
                if not ac.is_registered(admin, admin_code):
                    admin.add_admin()
            elif pick == 2:
                pass
            else:
                print("Invalid command!")
        else:
            print("Invalid command!")


if __name__ == '__main__':
    main()
