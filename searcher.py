from education import Classroom, Course
from people import Student, Admin, Teacher
from databases import MySQLConnector, create_database
import json


class Searcher:
    """
    A utility class for performing advanced searches and displaying data from various database tables.

    Attributes:
        DB (MySQLConnector): An instance of MySQLConnector for executing queries on the database.
    """
    
    with open("databases/db_info.json", "r") as file:
        db_info = json.load(file)
    DB = MySQLConnector(**db_info)

    @staticmethod
    def advanced_search(table, criteria=None):
        """
        Performs an advanced search on the specified database table based on multiple criteria.

        If no criteria are provided, returns all records from the specified table.

        :param table: A string representing the name of the database table to search.
        :param criteria: Optional. A dictionary containing the search criteria.
                         Example: {'class_name': 'Math', 'teacher_code': 123}
                         Keys represent column names in the table, and values represent desired values
                         for those columns in the search results.

        :return: A list of tuples containing the records that match the search criteria,
                 or all records from the specified table if no criteria are provided.
        """

        Searcher.DB = create_database.db

        if criteria is None or len(criteria) == 0:
            search_query = f"SELECT * FROM {table}"
        else:
            search_query = f"SELECT * FROM {table} WHERE "
            conditions = []

            for key, value in criteria.items():
                conditions.append(f"{key} = '{value}'")

            search_query += " AND ".join(conditions)

        try:
            result = Searcher.DB.execute_query(query=search_query)
            return result
        except:
            print(f"Search failed")
            return None

    @staticmethod
    def display_classroom(classrooms):
        Classroom.DB = create_database.db
        for classroom in classrooms:
            teacher = Teacher.search_by_code(classroom[5])
            course = Course.search_by_code(classroom[4])
            print("-"*17)
            print(f"Classroom name -> {classroom[1]}")
            print(f"Current enrollments -> {classroom[2]}")
            print(f"Teacher name -> {teacher[0][1]}")
            print(f"Course subject -> {course[0][1]}")
            print(f"Course capacity -> {course[0][3]}")
            print(f"Classroom code -> {classroom[3]}")

    @staticmethod
    def display_enrolled(enrolls):
        if not enrolls:
            print("Enrolls not found!")
            return

        for enroll in enrolls:
            print("-"*10)
            classroom = Classroom.search_by_code(enroll[2])
            student = Student.search_by_code(enroll[1])
            print(f"Student name: {student[0][1]}")
            print(f"Enrolled in {classroom[0][1]} class with code {enroll[2]}")
            print(f"Grade in this classroom -> {enroll[3]}")

    @staticmethod
    def display_student(students):
        Student.DB = create_database.db
        if not students:
            print("No students found!")
            return

        for student in students:
            print("-" * 17)
            print(f"Student name -> {student[1]}")
            print(f"Email -> {student[2]}")
            print(f"Gender -> {student[4]}")
            print(f"Student code -> {student[5]}")

    @staticmethod
    def display_teacher(teachers):
        Teacher.DB = create_database.db
        if not teachers:
            print("No teachers found!")
            return

        for teacher in teachers:
            print("-" * 17)
            print(f"Teacher name -> {teacher[1]}")
            print(f"Email -> {teacher[2]}")
            print(f"Gender -> {teacher[4]}")
            print(f"Teacher code -> {teacher[5]}")

    @staticmethod
    def display_course(courses):
        Course.DB = create_database.db
        if not courses:
            print("No courses found!")
            return

        for course in courses:
            print("-" * 17)
            print(f"Course name -> {course[1]}")
            print(f"Capacity -> {course[3]}")
            print(f"Course code -> {course[2]}")
