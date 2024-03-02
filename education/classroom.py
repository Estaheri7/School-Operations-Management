from databases import MySQLConnector
import pandas as pd
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

    @classmethod
    def search_by_code(cls, class_code):
        search_query = f"""
        SELECT * FROM classrooms
        WHERE class_code = {class_code}
        """
        try:
            result = cls.DB.execute_query(query=search_query)
            return result
        except:
            print("Something went wrong while searching...")
    @staticmethod
    def get_attrs(file=None):
        """
        Generates a list of Classroom objects based on user input or data from a CSV file.

        :param file: Optional. Path to a CSV file containing classroom data. If provided, classroom data will be
                     read from the file. If not provided, the user will be prompted to enter data for a single
                     classroom.

        :return: A list of Classroom objects generated from the provided data.
        """

        if file:
            classrooms = pd.read_csv(file)
            all_classrooms = []
            classrooms["current_enrollment"] = classrooms["current_enrollment"].astype(int)
            classrooms["class_code"] = classrooms["class_code"].astype(int)
            classrooms["course_code"] = classrooms["course_code"].astype(int)
            classrooms["teacher_code"] = classrooms["teacher_code"].astype(int)
            for _, classroom_data in classrooms.iterrows():
                new_classroom = Classroom(
                    classroom_data["name"],
                    classroom_data["current_enrollment"],
                    classroom_data["class_code"],
                    classroom_data["course_code"],
                    classroom_data["teacher_code"]
                )
                all_classrooms.append(new_classroom)
            return all_classrooms

        class_name = input("Enter name: ")
        current_enrollment = int(input("Enter current enrollment: "))
        class_code = input("Enter class code: ")
        course_code = input("Enter course code: ")
        teacher_code = input("Enter teacher code: ")
        classroom = Classroom(class_name, current_enrollment, class_code, course_code, teacher_code)
        return [classroom]
