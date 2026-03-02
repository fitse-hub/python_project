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
