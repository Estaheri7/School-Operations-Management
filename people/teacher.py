from .person import *


class Teacher(Person):
    def __init__(self, name, email, password, gender, teacher_code, department_id):
        super().__init__(name, email, password, gender)
        self.teacher_code = teacher_code
        self.department_id = department_id
