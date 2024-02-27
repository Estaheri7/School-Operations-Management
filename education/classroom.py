from databases import MySQLConnector
import json


class Classroom:
    with open("databases/db_info.json", "r") as file:
        db_info = json.load(file)
    DB = MySQLConnector(**db_info)

    def __init__(self, class_name, current_enrollment, class_code, course_code, teacher_code):
        """
        Initializes the Classroom object with the provided parameters.

        :param class_name: A string for setting name of the class.
        :param current_enrollment: Number of current enrollments.
        :param class_code: Unique parameter to set code for each classroom.
        :param course_code: foreign column from course object.
        :param teacher_code: foreign column from teacher object.
        """
        self.class_name = class_name
        self.current_enrollment = current_enrollment
        self.class_code = class_code
        self.course_code = course_code
        self.teacher_code = teacher_code

    def add_classroom(self):
        """
        Adds new classroom to school.
        """
        add_query = """
            INSERT INTO classrooms(name, current_enrollment, class_code, course_code, teacher_code)
            VALUES(%s, %s, %s, %s, %s);    
        """
        values = (
            self.class_name,
            self.current_enrollment,
            self.class_code,
            self.course_code,
            self.teacher_code
        )
        try:
            Classroom.DB.execute_query(query=add_query, params=values)
            Classroom.DB.commit()
        except:
            print("Failed to add classroom")

    @classmethod
    def remove_classroom(cls, class_code):
        """
        Removes a record of classroom from database.
        Records for enrolled students in this class will be removed from student_classes table.

        :param class_code: A unique code selected to remove classroom.
        """

        remove_query = """
        DELETE FROM classrooms WHERE class_code = (%s)
        """

        try:
            cls.DB.execute_query(query=remove_query, params=(class_code,))
            cls.DB.commit()
            print(f"Classroom with code {class_code} removed!")
        except:
            print("Failed to delete classroom!")
