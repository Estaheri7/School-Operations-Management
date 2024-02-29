from people.person import *


class Admin(Person):
    def __init__(self, name, email, password, gender):
        super().__init__(name, email, password, gender)


