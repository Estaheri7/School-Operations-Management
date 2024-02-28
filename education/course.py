from databases import MySQLConnector
import json


class Course:
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
        """
        query = """
            INSERT INTO courses(name, course_code, capacity)
            VALUES(%s, %s, %s);
        """
        values = (self.name, self.course_code, self.capacity)
        try:
            Course.DB.execute_query(query=query, params=values)
            Course.DB.commit()
        except:
            print("Failed to add course")

    @classmethod
    def remove_course(cls, course_code):
        """
        Removes a course record from database.
        If selected course is in a classroom, Its classroom will be deleted
        and records from student_classes for that class will be removed.

        :param course_code: A unique code to remove a course.
        """

        remove_query = """
        DELETE FROM courses WHERE course_code = (%s)
        """

        try:
            cls.DB.execute_query(query=remove_query, params=(course_code,))
            cls.DB.commit()
            print(f"Course with code {course_code} removed!")
        except:
            print("Failed to remove course!")

    @classmethod
    def update_course(cls, course_code, new_values):
        """
        Updates records for course by given parameters.

        :param course_code: The course code identifying the course to be updated.
        :param new_values: A tuple containing the new values for the course attributes
                           in the following order: (name, capacity).
        """
        
        update_query = f"""
        UPDATE courses
        SET name = %s, capacity = %s
        WHERE course_code = {course_code}
        """

        try:
            cls.DB.execute_query(query=update_query, params=new_values)
            cls.DB.commit()
            print(f"Records updated for course with code {course_code}")
        except:
            print("Failed to update course")
