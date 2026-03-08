# models.py - Data structures for the Course Registration System
#
# NOTE: Passwords are stored as SHA-256 hashes. The default admin password
# is "admin123" and should be changed in any non-demo environment.

# Default admin account (password: "admin123")
users = {
    "admin": {
        "password": "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9",
        "role": "admin"
    }
}

# students[student_id] = {"name": str, "registered_courses": [course_id, ...]}
students = {}

# courses[course_id] = {"name": str, "capacity": int, "enrolled_students": [student_id, ...]}
courses = {}

MAX_COURSES_PER_STUDENT = 5
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(password, hashed):
    return hash_password(password) == hashed


class Course:
    def __init__(self, course_id, name, code, capacity):
        self.course_id = course_id
        self.name = name
        self.code = code
        self.capacity = capacity
        self.enrolled_count = 0

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "name": self.name,
            "code": self.code,
            "capacity": self.capacity,
            "enrolled_count": self.enrolled_count,
        }

    @staticmethod
    def from_dict(data):
        course = Course(
            data["course_id"],
            data["name"],
            data["code"],
            data["capacity"],
        )
        course.enrolled_count = data.get("enrolled_count", 0)
        return course

    def is_available(self):
        return self.enrolled_count < self.capacity

    def __str__(self):
        status = "Available" if self.is_available() else "Full"
        return (
            f"[{self.code}] {self.name} "
            f"(Capacity: {self.enrolled_count}/{self.capacity} | {status})"
        )
class Course:
    def __init__(self, course_id, name, instructor, capacity):
        self.course_id = course_id
        self.name = name
        self.instructor = instructor
        self.capacity = capacity
        self.enrolled_count = 0

    def is_full(self):
        return self.enrolled_count >= self.capacity

    def __str__(self):
        return (f"[{self.course_id}] {self.name} | Instructor: {self.instructor} "
                f"| Seats: {self.capacity - self.enrolled_count}/{self.capacity}")


class Student:
    MAX_COURSES = 5

    def __init__(self, student_id, name, username, password, _hashed=False):
        self.student_id = student_id
        self.name = name
        self.username = username
        self.password = hash_password(password) if not _hashed else password
        self.enrolled_courses = []  # list of course_ids

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "username": self.username,
            "password": self.password,
            "enrolled_courses": self.enrolled_courses,
        }

    @staticmethod
    def from_dict(data):
        student = Student(
            data["student_id"],
            data["name"],
            data["username"],
            data["password"],
            _hashed=True,
        )
        student.enrolled_courses = data.get("enrolled_courses", [])
        return student


class Admin:
    def __init__(self, admin_id, name, username, password, _hashed=False):
        self.admin_id = admin_id
        self.name = name
        self.username = username
        self.password = hash_password(password) if not _hashed else password

    def to_dict(self):
        return {
            "admin_id": self.admin_id,
            "name": self.name,
            "username": self.username,
            "password": self.password,
        }

    @staticmethod
    def from_dict(data):
        return Admin(
            data["admin_id"],
            data["name"],
            data["username"],
            data["password"],
            _hashed=True,
        )
    def __init__(self, student_id, name, password):
        self.student_id = student_id
        self.name = name
        self.password = password
        self.registered_courses = []  # list of course_id strings

    def is_registered(self, course_id):
        return course_id in self.registered_courses

    def has_reached_limit(self):
        return len(self.registered_courses) >= self.MAX_COURSES
