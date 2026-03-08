import json
import os

STUDENTS_FILE = "students.json"
COURSES_FILE = "courses.json"
ADMINS_FILE = "admins.json"

from models import Student, Course, Admin


def _load_json(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def load_students():
    return [Student.from_dict(d) for d in _load_json(STUDENTS_FILE)]


def save_students(students):
    _save_json(STUDENTS_FILE, [s.to_dict() for s in students])


def load_courses():
    return [Course.from_dict(d) for d in _load_json(COURSES_FILE)]


def save_courses(courses):
    _save_json(COURSES_FILE, [c.to_dict() for c in courses])


def load_admins():
    admins = [Admin.from_dict(d) for d in _load_json(ADMINS_FILE)]
    if not admins:
        # Seed a default admin on first run
        default_admin = Admin("A001", "Admin", "admin", "admin123")
        save_admins([default_admin])
        return [default_admin]
    return admins


def save_admins(admins):
    _save_json(ADMINS_FILE, [a.to_dict() for a in admins])


def seed_courses():
    """Add sample courses if none exist."""
    courses = load_courses()
    if not courses:
        sample = [
            Course("C001", "Introduction to Python", "CS101", 30),
            Course("C002", "Data Structures", "CS201", 25),
            Course("C003", "Database Systems", "CS301", 20),
            Course("C004", "Operating Systems", "CS401", 20),
            Course("C005", "Software Engineering", "CS501", 35),
            Course("C006", "Computer Networks", "CS601", 25),
        ]
        save_courses(sample)
from models import Course, Student


class Storage:
    def __init__(self):
        self.courses = {
            "CS101": Course("CS101", "Introduction to Programming", "Dr. Smith", 30),
            "CS201": Course("CS201", "Data Structures", "Dr. Jones", 25),
            "CS301": Course("CS301", "Algorithms", "Dr. Brown", 20),
            "MATH101": Course("MATH101", "Calculus I", "Prof. Lee", 35),
            "MATH201": Course("MATH201", "Linear Algebra", "Prof. Chen", 30),
            "PHY101": Course("PHY101", "Physics I", "Dr. White", 28),
            "ENG101": Course("ENG101", "Technical Writing", "Ms. Davis", 40),
        }

        self.students = {
            "S001": Student("S001", "Alice", "alice123"),
            "S002": Student("S002", "Bob", "bob456"),
            "S003": Student("S003", "Carol", "carol789"),
        }

    def get_course(self, course_id):
        return self.courses.get(course_id)

    def get_student_by_id(self, student_id):
        return self.students.get(student_id)

    def find_student_by_name_and_password(self, name, password):
        for student in self.students.values():
            if student.name.lower() == name.lower() and student.password == password:
                return student
        return None

    def all_courses(self):
        return list(self.courses.values())
