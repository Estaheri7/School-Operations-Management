from .person import *


class Student(Person):
    def __init__(self, name, email, password, gender, student_code):
        super().__init__(name, email, password, gender)
        self.student_code = student_code
