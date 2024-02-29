tables = {
    "admins":
    """
    CREATE TABLE IF NOT EXISTS admins(
    admin_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    gender VARCHAR(255),
    PRIMARY KEY (admin_id)
    );
    """,
    "students":
    """
    CREATE TABLE IF NOT EXISTS students(
    student_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    gender VARCHAR(255),
    student_code INT NOT NULL UNIQUE,
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
    teacher_code INT NOT NULL UNIQUE,
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
    teacher_code INT NOT NULL,
    PRIMARY KEY (classroom_id),
    FOREIGN KEY (course_code) REFERENCES courses (course_code)
        ON DELETE CASCADE,
    FOREIGN KEY (teacher_code) REFERENCES teachers (teacher_code)
        ON DELETE CASCADE
    );
    """,
    "student_classes":
    """
    CREATE TABLE IF NOT EXISTS student_classes(
    student_class_id INT NOT NULL AUTO_INCREMENT,
    student_code INT NOT NULL,
    class_code INT NOT NULL,
    grade INT,
    PRIMARY KEY (student_class_id),
    FOREIGN KEY (student_code) REFERENCES students (student_code)
        ON DELETE CASCADE,
    FOREIGN KEY (class_code) REFERENCES classrooms (class_code)
        ON DELETE CASCADE
    );
    """
}
