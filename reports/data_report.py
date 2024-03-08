from search import Searcher
from education import Classroom
import matplotlib.pyplot as plt
import pandas as pd


class DataReport:
    """
    A class for generating data reports and visualizations.

    Attributes:
        title (str): The title of the visualization.
        xlabel (str): The label for the x-axis.
        ylabel (str): The label for the y-axis.
        color (str): The color of the data points.
        figsize (tuple): The size of the figure (width, height) in inches.
    """

    def __init__(self, title='', xlabel='', ylabel='', color='green', figsize=(5, 5)):
        """
        Initializes a DataReport object with the provided attributes.

        Args:
            title (str): The title of the visualization.
            xlabel (str): The label for the x-axis.
            ylabel (str): The label for the y-axis.
            color (str, optional): The color of the data points. Defaults to 'green'.
            figsize (tuple, optional): The size of the figure (width, height) in inches. Defaults to (5, 5).
        """

        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.color = color
        self.figsize = figsize

    def visualize_grade_distribution(self, class_code, teacher_code):
        """
        Visualizes the grade distribution of students in a classroom.

        Args:
            class_code (str): The code of the classroom to visualize.
            teacher_code (str): The code of the teacher who owns the classroom.

        Raises:
            ValueError: If the specified classroom or teacher is not found.
        """

        try:
            # checking if given class_code exists
            result = Classroom.search_by_code(class_code)
            if not result:
                print("Classroom not found!")
                return

            # checking if teacher who sent class code owns the class
            if teacher_code != result[0][5]:
                print("You don't own this classroom!")
                return

            # retrieve enrollment data for the class
            enrolls = Searcher.advanced_search("student_classes", {"class_code": class_code})
            if not enrolls:
                print("Enrolls not found!")
                return
            student_codes = [str(enroll[1]) for enroll in enrolls]
            grades = [enroll[3] if enroll[3] is not None else 0 for enroll in enrolls]

            # create scatter plot for grade distribution
            plt.figure(figsize=self.figsize)
            plt.scatter(student_codes, grades, color=self.color, alpha=0.5)
            plt.title(self.title)
            plt.xlabel(self.xlabel)
            plt.ylabel(self.ylabel)
            plt.grid(True)

            plt.show()
        except Exception as e:
            raise e

    def visualize_enrollment_distribution(self):
        """
        Visualizes the distribution of current enrollment across all classrooms.

        Retrieves the current enrollment data for all classrooms using the Searcher class.
        Constructs a bar plot where each bar represents a classroom, with the height of the bar
        indicating the current enrollment count for that classroom.

        :return: None
        """

        try:
            # search for classroom if exists...
            classrooms = Searcher.advanced_search("classrooms")
            if not classrooms:
                print("Classrooms not found!")
                return

            # collecting class_codes
            class_codes = [str(enrollment[3]) for enrollment in classrooms]
            # collecting enrollment numbers
            current_enrollments = [str(enrollment[2]) for enrollment in classrooms]

            # create bar plot for enrollment distribution
            plt.figure(figsize=self.figsize)
            plt.bar(class_codes, current_enrollments, color=self.color)
            plt.title(self.title)
            plt.xlabel(self.xlabel)
            plt.ylabel(self.ylabel)

            plt.show()
        except Exception as e:
            raise e

    def analyze_teacher_workload(self):
        """
        Analyzes and visualizes the workload of teachers by calculating the number of courses and total students
        per teacher. Utilizes pandas to perform calculations and matplotlib to visualize the workload.

        :return: None
        """

        try:
            # searching for classroom if exists...
            classrooms = Searcher.advanced_search("classrooms")
            if not classrooms:
                print("Classrooms not found!")
                return

            # converting classroom data to DataFrame
            df = pd.DataFrame(classrooms,
                              columns=['class_id', 'class_name', 'current_enrollment', 'class_code', 'course_code',
                                       'teacher_code'])

            # group data by teacher and aggregate course count and total students
            teacher_workload = df.groupby('teacher_code').agg(
                {'course_code': 'nunique', 'current_enrollment': 'sum'}).reset_index()
            teacher_workload.columns = ['teacher_code', 'num_courses', 'total_students']

            # retrieve teacher names from Searcher
            teacher_names = {teacher[5]: teacher[1] for teacher in Searcher.advanced_search("teachers")}

            # map teacher names to teacher workload DataFrame
            teacher_workload['teacher_name'] = teacher_workload['teacher_code'].map(teacher_names)

            # create bar plot for teacher workload
            plt.figure(figsize=self.figsize)
            plt.bar(teacher_workload['teacher_name'], teacher_workload['num_courses'], color='blue',
                    label='Number of Courses')
            plt.bar(teacher_workload['teacher_name'], teacher_workload['total_students'], color='orange',
                    label='Total Students')
            plt.title(self.title)
            plt.xlabel(self.xlabel)
            plt.ylabel(self.ylabel)
            plt.xticks(rotation=45, ha='right')
            plt.legend()
            plt.tight_layout()
            plt.show()
        except Exception as e:
            raise e
