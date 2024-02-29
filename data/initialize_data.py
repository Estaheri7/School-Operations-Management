import json
from education import Classroom, Course
from people import Teacher, Student, Admin


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
        teacher.add_teacher()

    for c in courses:
        course = Course(c["name"], c["course_code"], c["capacity"])
        course.add_course()

    for r in classrooms:
        classroom = Classroom(r["name"], r["current_enrollment"],
                              r["class_code"], r["course_code"], r["teacher_code"])
        classroom.add_classroom()

    for s in students:
        student = Student(s["name"], s["email"], s["password"], s["gender"], s["student_code"])
        student.add_student()

    for a in admins:
        admin = Admin(a["name"], a["email"], a["password"], a["gender"])
        admin.add_admin()
