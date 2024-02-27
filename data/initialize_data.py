import json
from education import Classroom, Course
from people import Teacher


def initialize_data(database, classrooms, courses, teachers):
    with open(classrooms, "r") as file:
        classrooms = json.load(file)

    with open(courses, "r") as file:
        courses = json.load(file)

    with open(teachers, "r") as file:
        teachers = json.load(file)

    for t in teachers:
        teacher = Teacher(
            t["name"],
            t["email"],
            t["password"],
            t["gender"],
            t["teacher_code"],
            t["department_id"]
        )
        teacher.add_teacher(database)

    for c in courses:
        course = Course(c["name"], c["course_code"], c["capacity"])
        course.add_course(database)

    for r in classrooms:
        classroom = Classroom(r["name"], r["current_enrollment"],
                              r["class_code"], r["course_code"], r["teacher_code"])
        classroom.add_classroom(database)

