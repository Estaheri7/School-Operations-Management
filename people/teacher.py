from .person import *


class Teacher(Person):
    teacher_id = 0

    def __init__(self, name, email, password, gender):
        super().__init__(name, email, password, gender)
        Teacher.teacher_id += 1
