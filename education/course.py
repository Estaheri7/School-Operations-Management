class Course:
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

    def add_course(self, database):
        """
        Adds new course to school.

        :param database: A MySQLConnector object which is connected to database.
        """
        query = """
            INSERT INTO courses(name, course_code, capacity)
            VALUES(%s, %s, %s);
        """
        values = (self.name, self.course_code, self.capacity)
        try:
            database.execute_query(query=query, params=values)
            database.commit()
        except:
            print("Failed to add course")

    @staticmethod
    def remove_course(database, course_code):
        """
        Removes a course record from database.

        :param database: A MySQLConnector object which is connected to database.
        :param course_code: A unique code to remove a course.
        """

        remove_query = """
        DELETE FROM courses WHERE course_code = (%s)
        """

        try:
            database.execute_query(query=remove_query, params=(course_code,))
            database.commit()
            print(f"Course with code {course_code} removed!")
        except:
            print("Failed to remove course!")
