# School Operations Management

School Management System is a Python-based application designed to streamline administrative
tasks in educational institutions. It offers functionalities for managing student, teacher, and
admin accounts, handling enrollments, grading, and generating insightful reports. Whether you're a
student, teacher, or administrator, this system provides an intuitive interface to manage 
academic activities efficiently.

## Features

- **Student Management:**
  - Allows students to register.
  - Enroll in classes.
  - View their enrollments.
  - Drop classes.

- **Teacher Management:**
  - Enables teachers to register.
  - Add grades for students.
  - View enrollments of their classes.

- **Admin Panel**: Provides administrators with functionalities to manage students, teachers, classrooms, courses, and generate reports.
- **Search Functionality**: Allows searching for specific records in the database based on different criteria.
- **Data Visualization**: Generates visual reports such as grade distribution and enrollment distribution using matplotlib.

## Project Structure

- **data**: Contains JSON files for initializing data.
- **databases**: Contains scripts for database connection and creation.
- **people**: Includes classes for different user roles (Admin, Student, Teacher, Person).
- **account_management**: Contains classes for managing user accounts and authentication.
- **search**: Includes a class for searching database records.
- **reports**: Contains classes for generating data reports.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/Estaheri7/School-Operations-Management.git
    cd school-operations-management
    ```

2. Install the required Libraries/Frameworks:
    ```bash
    pip install -r requirements.txt
    ```
   
3. Run the main script:
    ```bash
    Python main.py
    ```
   
## Usage

Upon running the main script, you will be prompted to select your role (Student, Teacher, Admin) and
either register or login. Follow the prompts to navigate through the application functionalities based on
your role


