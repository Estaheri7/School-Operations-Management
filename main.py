from databases import MySQLConnector, tables, create_database
from data.initialize_data import *


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

    login = False
    while True:
        role = input("Select your role (Student, Teacher, Admin) or -1 to exit: ").lower()

        if role == "student":
            pass
        elif role == "teacher":
            pass
        elif role == "admin":
            pass
        elif role == "-1":
            pass
        else:
            print("Invalid command!")


if __name__ == '__main__':
    main()
