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

        :raise Exception: If classroom cannot be added.
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
            print("Classroom added successfully!")
        except Exception as e:
            raise e

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

    @classmethod
    def update_classroom(cls, class_code, new_values):
        """
        Updates records for classroom by given parameters.

        :param class_code: The class code identifying the classroom to be updated.
        :param new_values: A tuple containing the new values for the classroom attributes
                           in the following order: (name, current_enrollment, course_code, teacher_code).
        """

        update_query = f"""
        UPDATE classrooms
        SET name = %s, current_enrollment = %s, course_code = %s, teacher_code = %s
        WHERE class_code = {class_code}
        """

        try:
            cls.DB.execute_query(query=update_query, params=new_values)
            cls.DB.commit()
            print(f"Records updated for classroom with code {class_code}")
        except:
            print("Failed to update records")
