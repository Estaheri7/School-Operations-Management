from .person import *


class Student(Person):
    student_id = 0

    def __init__(self, name, email, password, gender):
        super().__init__(name, email, password, gender)
        Student.student_id += 1
