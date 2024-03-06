from abc import ABC, abstractmethod
from databases import MySQLConnector
import json


class Person(ABC):
    with open("databases/db_info.json", "r") as file:
        db_info = json.load(file)
    DB = MySQLConnector(**db_info)

    def __init__(self, name, email, password, gender):
        self.name = name
        self.email = email
        self.password = password
        self.gender = gender

    @staticmethod
    def remove_person(person_code):
        pass

