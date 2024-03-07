import json
from education import Classroom, Course
from people import Teacher, Student, Admin

# This file only initializes data for testing program.
# initialize_data reads json files in this data folder and then uses method to add them to database


def initialize_data(classrooms, courses, teachers, students, admins):
    with open(classrooms, "r") as file:
        classrooms = json.load(file)

    with open(courses, "r") as file:
        courses = json.load(file)

    with open(teachers, "r") as file:
        teachers = json.load(file)

    with open(students, "r") as file:
        students = json.load(file)

    with open(admins, "r") as file:
        admins = json.load(file)

    for t in teachers:
        teacher = Teacher(
            t["name"],
            t["email"],
            t["password"],
            t["gender"],
            t["teacher_code"],
            t["department_id"]
        )
        try:
            teacher.add_teacher()
        except:
            pass

    for c in courses:
        course = Course(c["name"], c["course_code"], c["capacity"])
        try:
            course.add_course()
        except:
            pass

    for r in classrooms:
        classroom = Classroom(r["name"], r["current_enrollment"],
                              r["class_code"], r["course_code"], r["teacher_code"])
        try:
            classroom.add_classroom()
        except:
            pass

    for s in students:
        student = Student(s["name"], s["email"], s["password"], s["gender"], s["student_code"])
        try:
            student.add_student()
        except:
            pass

    for a in admins:
        admin = Admin(a["name"], a["email"], a["password"], a["gender"], a["admin_code"])
        try:
            admin.add_admin()
        except:
            pass
