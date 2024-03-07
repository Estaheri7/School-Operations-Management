from databases import MySQLConnector
import pandas as pd
import json


class Course:
    """
    A class representing a course in a school, including methods to add, remove, update, and search for courses
    in the database.

    Attributes:
        DB (MySQLConnector): A MySQLConnector object for interacting with the database.
    """

    # connect class attribute DB to database
    with open("databases/db_info.json", "r") as file:
        db_info = json.load(file)
    DB = MySQLConnector(**db_info)

    def __init__(self, name, course_code, capacity):
        """
        Initializes the Course object with the provided parameters.

        :param name: A name for each course object.
        :param course_code: A unique value for each course.
        :param capacity: Maximum number of enrollments.
        """
        self.name = name
        self.course_code = course_code
        self.capacity = capacity

    def add_course(self):
        """
        Adds new course to school.

        :raise Exception: If course cannot be added.
        """
        query = """
            INSERT INTO courses(name, course_code, capacity)
            VALUES(%s, %s, %s);
        """
        values = (self.name, self.course_code, self.capacity)
        try:
            Course.DB.execute_query(query=query, params=values)
            Course.DB.commit()
            print("Course added successfully!")
        except Exception as e:
            raise e

    @classmethod
    def remove_course(cls, course_code):
        """
        Removes a course record from database.
        If selected course is in a classroom, Its classroom will be deleted
        and records from student_classes for that class will be removed.

        :param course_code: A unique code to remove a course.
        """

        # Searching for course...
        result = Course.search_by_code(course_code)
        if not result:
            print("Course not found!")
            return

        remove_query = """
        DELETE FROM courses WHERE course_code = (%s)
        """

        try:
            cls.DB.execute_query(query=remove_query, params=(course_code,))
            cls.DB.commit()
            print(f"Course with code {course_code} removed!")
        except Exception as e:
            print("Failed to remove course!")
            raise e

    @classmethod
    def update_course(cls, course_code, new_values):
        """
        Updates records for course by given parameters.

        :param course_code: The course code identifying the course to be updated.
        :param new_values: A tuple containing the new values for the course attributes
                           in the following order: (name, capacity).
        """

        # Searching for course...
        result = Course.search_by_code(course_code)
        if not result:
            print("Course not found!")
            return

        update_query = f"""
        UPDATE courses
        SET name = %s, capacity = %s
        WHERE course_code = {course_code}
        """

        try:
            cls.DB.execute_query(query=update_query, params=new_values)
            cls.DB.commit()
            print(f"Records updated for course with code {course_code}")
        except Exception as e:
            print("Failed to update course")
            raise e

    @classmethod
    def search_by_code(cls, course_code):
        """
        Searches for a course in the database by its course code.

        :param course_code: The unique code identifying the course.

        :return: A list of tuples containing the details of the course if found, otherwise None.

        Executes a SQL query to retrieve the details of the course with the provided course code.
        Returns the result of the query if a course with the given code is found,
        otherwise returns None.
        """
        search_query = f"""
        SELECT * FROM courses
        WHERE course_code = {course_code}
        """

        try:
            result = cls.DB.execute_query(query=search_query)
            return result
        except Exception as e:
            print("Something went wrong while searching...")
            raise e

    @staticmethod
    def get_attrs(file=None):
        """
        Generate a list of Course objects based on user input or data from a CSV file.

        :param file: Optional. Path to a CSV file containing course data. If provided, course data will be
                     read from the file. If not provided, the user will be prompted to enter data for a single
                     course.

        :return: A list of Course objects generated from the provided data.
        """
        
        if file:
            try:
                # read courses csv file using pandas
                courses = pd.read_csv(file)
                # an empty list to collect courses
                all_courses = []
                # convert numpy int to mysql int
                courses["course_code"] = courses["course_code"].astype(int)
                courses["capacity"] = courses["capacity"].astype(int)
                for _, course_data in courses.iterrows():
                    # create course object
                    new_course = Course(
                        course_data["name"],
                        course_data["course_code"],
                        course_data["capacity"],
                    )
                    # add created object to created list
                    all_courses.append(new_course)
                return all_courses
            except FileNotFoundError as e:
                print("File not found!")
        name = input("Enter name: ")
        course_code = input("Enter course code: ")
        capacity = int(input("Enter capacity: "))
        course = Course(name, course_code, capacity)
        return [course]
