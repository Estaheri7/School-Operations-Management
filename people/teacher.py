from .person import *


class Teacher(Person):
    teacher_id = 0

    def __init__(self, name, email, password, gender, department_id):
        super().__init__(name, email, password, gender)
        self.department_id = department_id
        Teacher.teacher_id += 1
