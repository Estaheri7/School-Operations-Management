from searcher import Searcher
from education import Classroom
import matplotlib.pyplot as plt


class DataReport:
    def __init__(self, title='', xlabel='', ylabel='', color='green', figsize=(5, 5)):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.color = color
        self.figsize = figsize

    def visualize_grade_distribution(self, class_code, teacher_code):
        result = Classroom.search_by_code(class_code)
        if not result:
            print("Classroom not found!")
            return

        if teacher_code != result[0][5]:
            print("You don't own this classroom!")
            return

        enrolls = Searcher.advanced_search("student_classes", {"class_code": class_code})
        if not enrolls:
            print("Enrolls not found!")
            return
        student_codes = [str(enroll[1]) for enroll in enrolls]
        grades = [enroll[3] if enroll[3] is not None else 0 for enroll in enrolls]

        plt.figure(figsize=self.figsize)
        plt.scatter(student_codes, grades, color=self.color, alpha=0.5)
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.grid(True)

        plt.show()
