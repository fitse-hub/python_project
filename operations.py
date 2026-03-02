# operations.py - Business logic for the Course Registration System

import hashlib

from models import users, students, courses, MAX_COURSES_PER_STUDENT


def _hash_password(password):
    """Return a SHA-256 hex digest of the given password."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Admin operations
# ---------------------------------------------------------------------------

def add_student(student_id, name, password):
    """Add a new student. Returns (True, message) or (False, error)."""
    if not student_id or not name or not password:
        return False, "All fields (ID, name, password) are required."
    if student_id in students:
        return False, f"Student ID '{student_id}' already exists."
    if student_id in users:
        return False, f"Username '{student_id}' already in use."

    students[student_id] = {"name": name, "registered_courses": []}
    users[student_id] = {"password": _hash_password(password), "role": "student"}
    return True, f"Student '{name}' (ID: {student_id}) added successfully."


def add_course(course_id, name, capacity):
    """Add a new course. Returns (True, message) or (False, error)."""
    if not course_id or not name:
        return False, "Course ID and name are required."
    if course_id in courses:
        return False, f"Course ID '{course_id}' already exists."
    try:
        capacity = int(capacity)
        if capacity <= 0:
            raise ValueError
    except ValueError:
        return False, "Capacity must be a positive integer."

    courses[course_id] = {"name": name, "capacity": capacity, "enrolled_students": []}
    return True, f"Course '{name}' (ID: {course_id}, Capacity: {capacity}) added successfully."


def view_all_students():
    """Return a formatted string listing all students."""
    if not students:
        return "No students registered yet."
    lines = ["\n{:<15} {:<25} {:<10}".format("Student ID", "Name", "Courses"),
             "-" * 55]
    for sid, info in students.items():
        lines.append("{:<15} {:<25} {:<10}".format(
            sid, info["name"], len(info["registered_courses"])
        ))
    return "\n".join(lines)


def view_all_courses():
    """Return a formatted string listing all courses."""
    if not courses:
        return "No courses available yet."
    lines = ["\n{:<12} {:<30} {:<10} {:<10} {:<10}".format(
        "Course ID", "Name", "Capacity", "Enrolled", "Remaining"),
        "-" * 75]
    for cid, info in courses.items():
        enrolled = len(info["enrolled_students"])
        remaining = info["capacity"] - enrolled
        lines.append("{:<12} {:<30} {:<10} {:<10} {:<10}".format(
            cid, info["name"], info["capacity"], enrolled, remaining
        ))
    return "\n".join(lines)


def view_enrollment_reports():
    """Return a formatted enrollment report for admin."""
    if not courses and not students:
        return "No data available for reports."

    lines = ["\n" + "=" * 60,
             " COURSE ENROLLMENT REPORT",
             "=" * 60]

    # Course report
    lines.append("\n📊 COURSE REPORT")
    lines.append("-" * 60)
    if courses:
        for cid, info in courses.items():
            enrolled = len(info["enrolled_students"])
            remaining = info["capacity"] - enrolled
            lines.append(f"\nCourse ID : {cid}")
            lines.append(f"  Name      : {info['name']}")
            lines.append(f"  Capacity  : {info['capacity']}")
            lines.append(f"  Enrolled  : {enrolled}")
            lines.append(f"  Remaining : {remaining}")
            if info["enrolled_students"]:
                student_names = [
                    students[s]["name"] for s in info["enrolled_students"] if s in students
                ]
                lines.append(f"  Students  : {', '.join(student_names)}")
            else:
                lines.append("  Students  : None")
    else:
        lines.append("  No courses available.")

    # Student report
    lines.append("\n📊 STUDENT REPORT")
    lines.append("-" * 60)
    if students:
        for sid, info in students.items():
            lines.append(f"\nStudent ID : {sid}")
            lines.append(f"  Name     : {info['name']}")
            lines.append(f"  Courses  : {len(info['registered_courses'])}")
            if info["registered_courses"]:
                course_names = [
                    f"{cid} - {courses[cid]['name']}"
                    for cid in info["registered_courses"]
                    if cid in courses
                ]
                lines.append(f"  Enrolled : {', '.join(course_names)}")
            else:
                lines.append("  Enrolled : None")
    else:
        lines.append("  No students registered.")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Student operations
# ---------------------------------------------------------------------------

def register_course(student_id, course_id):
    """Enroll a student in a course. Returns (True, message) or (False, error)."""
    if student_id not in students:
        return False, "Student not found."
    if course_id not in courses:
        return False, f"Course ID '{course_id}' does not exist."

    student = students[student_id]
    course = courses[course_id]

    if course_id in student["registered_courses"]:
        return False, f"You are already enrolled in '{course['name']}'."

    if len(student["registered_courses"]) >= MAX_COURSES_PER_STUDENT:
        return False, (
            f"Maximum course limit ({MAX_COURSES_PER_STUDENT}) reached. "
            "Drop a course before registering a new one."
        )

    enrolled = len(course["enrolled_students"])
    if enrolled >= course["capacity"]:
        return False, f"Course '{course['name']}' is full (capacity: {course['capacity']})."

    student["registered_courses"].append(course_id)
    course["enrolled_students"].append(student_id)
    return True, f"Successfully enrolled in '{course['name']}'."


def drop_course(student_id, course_id):
    """Drop a course for a student. Returns (True, message) or (False, error)."""
    if student_id not in students:
        return False, "Student not found."
    if course_id not in courses:
        return False, f"Course ID '{course_id}' does not exist."

    student = students[student_id]
    course = courses[course_id]

    if course_id not in student["registered_courses"]:
        return False, f"You are not enrolled in '{course['name']}'."

    student["registered_courses"].remove(course_id)
    if student_id in course["enrolled_students"]:
        course["enrolled_students"].remove(student_id)
    return True, f"Successfully dropped '{course['name']}'."


def view_my_courses(student_id):
    """Return a formatted list of courses a student is enrolled in."""
    if student_id not in students:
        return "Student not found."

    student = students[student_id]
    registered = student["registered_courses"]

    if not registered:
        return "You are not enrolled in any courses yet."

    lines = [f"\nCourses for {student['name']} (ID: {student_id}):",
             "-" * 50,
             "{:<12} {:<30}".format("Course ID", "Course Name"),
             "-" * 50]
    for cid in registered:
        if cid in courses:
            lines.append("{:<12} {:<30}".format(cid, courses[cid]["name"]))
    lines.append("-" * 50)
    lines.append(f"Total registered: {len(registered)}/{MAX_COURSES_PER_STUDENT}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Search (bonus)
# ---------------------------------------------------------------------------

def search_course(query):
    """Search courses by ID or name. Returns formatted results."""
    query_lower = query.lower()
    results = {
        cid: info for cid, info in courses.items()
        if query_lower in cid.lower() or query_lower in info["name"].lower()
    }
    if not results:
        return f"No courses found matching '{query}'."

    lines = ["\nSearch Results:",
             "{:<12} {:<30} {:<10} {:<10}".format(
                 "Course ID", "Name", "Capacity", "Enrolled"),
             "-" * 65]
    for cid, info in results.items():
        enrolled = len(info["enrolled_students"])
        lines.append("{:<12} {:<30} {:<10} {:<10}".format(
            cid, info["name"], info["capacity"], enrolled
        ))
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

def authenticate(username, password):
    """Return (role, message) if valid, or (None, error) if invalid."""
    if username not in users:
        return None, "Username not found."
    if users[username]["password"] != _hash_password(password):
        return None, "Incorrect password."
    return users[username]["role"], "Login successful."
