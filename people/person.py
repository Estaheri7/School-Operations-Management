from abc import ABC, abstractmethod


class Person(ABC):
    def __init__(self, name, email, password, gender):
        self.name = name
        self.email = email
        self.password = password
        self.gender = gender

    @staticmethod
    def remove_person(database, person_code):
        pass

