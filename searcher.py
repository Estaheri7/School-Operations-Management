from education import Classroom, Course
from people import Student, Admin, Teacher


class Searcher:
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

        if criteria is None or len(criteria) == 0:
            search_query = f"SELECT * FROM {table}"
        else:
            search_query = f"SELECT * FROM {table} WHERE "
            conditions = []

            for key, value in criteria.items():
                conditions.append(f"{key} = '{value}'")

            search_query += " AND ".join(conditions)

        try:
            result = Classroom.DB.execute_query(query=search_query)
            return result
        except:
            print(f"Search failed")
            return None
