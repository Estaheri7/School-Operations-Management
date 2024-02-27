class Classroom:
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

    def add_classroom(self, database):
        """
        Adds new classroom to school.

        :param database: A MySQLConnector object which is connected to database.
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
            database.execute_query(query=add_query, params=values)
            database.commit()
        except:
            print("Failed to add classroom")

    @staticmethod
    def remove_classroom(database, class_code):
        """
        Removes a record of classroom from database.
        Records for enrolled students in this class will be removed from student_classes table.

        :param database: A MySQLConnector object which is connected to database.
        :param class_code: A unique code selected to remove classroom.
        """

        remove_query = """
        DELETE FROM classrooms WHERE class_code = (%s)
        """

        try:
            database.execute_query(query=remove_query, params=(class_code,))
            database.commit()
            print(f"Classroom with code {class_code} removed!")
        except:
            print("Failed to delete classroom!")
