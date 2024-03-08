from databases import create_database
from people import Admin, Student, Teacher, Person
from data.initialize_data import initialize_data
from account_management import *
from search import Searcher
from reports import DataReport


def main() -> None:
    database = create_database.db
    initialize_data(
        r"data\classrooms.json",
        r"data\courses.json",
        r"data\teachers.json",
        r"data\students.json",
        r"data\admins.json"
    )

    AM = AccountManager(database)

    login = False
    while True:
        role = input("Select your role (Student, Teacher, Admin) or -1 to exit: ").lower()
        if role == "-1":
            break

        pick = int(input("Enter 1 to register or 2 to login: "))

        if role == "student":
            Person.DB = create_database.db
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
                    Searcher.display_classroom(Searcher.advanced_search("classrooms"))
                    class_code = input("Enter class code: ")
                    current_student.enroll(class_code)
                elif choice == 2:
                    print("Your enrollments: ")
                    conditions = {"student_code": current_student.student_code}
                    Searcher.display_enrolled(Searcher.advanced_search("student_classes", conditions))
                    class_code = input("Enter class code: ")
                    current_student.delete_enrollment(class_code)
                elif choice == 3:
                    report = DataReport(
                        "Class Enrollment Distribution",
                        "Class Code",
                        "Enrollments",
                        ["purple", "blue"],
                        (7, 7)
                    )
                    report.visualize_enrollment_distribution()
                else:
                    print("Invalid command!")
        elif role == "teacher":
            Person.DB = create_database.db
            current_teacher = None
            if pick == 1:
                teacher = Teacher.get_attrs()
                print("Going to if..")
                if not AM.is_registered(teacher[0], teacher[0].teacher_code):
                    teacher[0].add_teacher()
                    print("Added")
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
                    while new_grade < 0 or new_grade > 20:
                        print("Invalid value for grade!")
                        new_grade = int(input("Grade must be between 0 and 20: "))
                    current_teacher.add_grade(student_code, class_code, new_grade)
                elif choice == 2:
                    conditions = {"teacher_code": current_teacher.teacher_code}
                    all_classrooms = Searcher.advanced_search("classrooms", conditions)
                    class_code = set()
                    for classroom in all_classrooms:
                        class_code.add(classroom[3])
                    for code in class_code:
                        condition = {"class_code": code}
                        Searcher.display_enrolled(Searcher.advanced_search("student_classes", condition))
                elif choice == 3:
                    report = DataReport(
                        "Grade Distribution by Student Code",
                        "Student Code",
                        "Grade",
                        figsize=(7, 7)
                    )
                    class_code = input("Enter your class code: ")
                    report.visualize_grade_distribution(class_code, current_teacher.teacher_code)
                else:
                    print("Invalid command!")
        elif role == "admin":
            Person.DB = create_database.db
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
                    print("Students:")
                    Searcher.display_student(Searcher.advanced_search("students"))
                    Admin.do_object("student")
                elif choice == 2:
                    Searcher.display_teacher(Searcher.advanced_search("teachers"))
                    Admin.do_object("teacher")
                elif choice == 3:
                    Searcher.display_classroom(Searcher.advanced_search("classrooms"))
                    Admin.do_object("classroom")
                elif choice == 4:
                    Searcher.display_course(Searcher.advanced_search("courses"))
                    Admin.do_object("course")
                elif choice == 5:
                    criteria = {}
                    table = input("Enter table name to search it: ")
                    tbs = ["classrooms", "courses", "students", "teachers", "admins", "student_classes"]
                    if table not in tbs:
                        print(tbs)
                        table = input("Please select one of these: ")
                    while True:
                        key = input("Enter the column name (key) to search (or press Enter to stop): ").strip()
                        if not key:
                            break
                        value = input("Enter the value to search for: ")
                        criteria[key] = value

                    print("Searching...")
                    results = Searcher.advanced_search(table, criteria)
                    if results:
                        print("Search Results:")
                        if table == "classrooms":
                            Searcher.display_classroom(results)
                        elif table == "students":
                            Searcher.display_student(results)
                        elif table == "teachers":
                            Searcher.display_teacher(results)
                        elif table == "courses":
                            Searcher.display_course(results)
                    else:
                        print("No matching records found.")
                elif choice == 6:
                    report = DataReport(
                        "Teacher Workload",
                        "Teachers",
                        "Course - Students",
                        figsize=(7, 7)
                    )
                    report.analyze_teacher_workload()
                else:
                    print("Invalid command!")
        else:
            print("Invalid command!")


if __name__ == '__main__':
    main()
