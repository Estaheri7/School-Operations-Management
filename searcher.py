from education import Classroom, Course
from people import Student, Admin, Teacher
from databases import MySQLConnector, create_database
import json


class Searcher:
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
            print(f"Enrolled in {classroom[0][1]} class with code {enroll[2]}")
            print(f"Grade in this classroom -> {enroll[3]}")
