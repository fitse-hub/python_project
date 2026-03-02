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
