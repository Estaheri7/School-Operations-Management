tables = {
    "students":
    """
    CREATE TABLE IF NOT EXISTS students(
    student_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    gender VARCHAR(255),
    PRIMARY KEY (student_id)
    );
    """,
    "teachers":
    """
    CREATE TABLE IF NOT EXISTS teachers(
    teacher_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    gender VARCHAR(255),
    department_id INT UNIQUE,
    PRIMARY KEY (teacher_id)
    );
    """,
    "courses":
    """
    CREATE TABLE IF NOT EXISTS courses(
    course_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    course_code INT NOT NULL UNIQUE,
    capacity INT NOT NULL,
    PRIMARY KEY (course_id)
    );
    """,
    "classrooms":
    """
    CREATE TABLE IF NOT EXISTS classrooms(
    classroom_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    current_enrollment INT NOT NULL,
    class_code INT NOT NULL UNIQUE,
    course_code INT NOT NULL,
    teacher_id INT NOT NULL,
    PRIMARY KEY (classroom_id),
    FOREIGN KEY (course_code) REFERENCES courses (course_code)
        ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES teachers (teacher_id)
        ON DELETE CASCADE
    );
    """,
    "student_classes":
    """
    CREATE TABLE IF NOT EXISTS student_classes(
    student_class_id INT NOT NULL AUTO_INCREMENT,
    student_id INT NOT NULL,
    class_id INT NOT NULL,
    PRIMARY KEY (student_class_id),
    FOREIGN KEY (student_id) REFERENCES students (student_id)
        ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classrooms (classroom_id)
        ON DELETE CASCADE
    );
    """,

    "teacher_classes":
    """
    CREATE TABLE IF NOT EXISTS teacher_classes(
    teacher_class_id INT NOT NULL AUTO_INCREMENT,
    teacher_id INT NOT NULL,
    class_id INT NOT NULL,
    PRIMARY KEY (teacher_class_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers (teacher_id)
        ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classrooms (classroom_id)
        ON DELETE CASCADE
    );
    """
}
