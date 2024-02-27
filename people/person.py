from abc import ABC, abstractmethod


class Person(ABC):
    def __init__(self, name, email, password, gender):
        self.name = name
        self.email = email
        self.password = password
        self.gender = gender

    @classmethod
    def remove_person(cls, person_code):
        pass

