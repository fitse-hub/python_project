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
from storage import (
    load_students, save_students,
    load_courses, save_courses,
    load_admins, save_admins,
)
from models import Student, Course, Admin, check_password


# ── Utility helpers ────────────────────────────────────────────────────────────

def _find_student(username):
    for s in load_students():
        if s.username == username:
            return s
    return None


def _find_course_by_id(course_id):
    for c in load_courses():
        if c.course_id == course_id:
            return c
    return None


def _find_course_by_code(code):
    for c in load_courses():
        if c.code.lower() == code.lower():
            return c
    return None


# ── Authentication ─────────────────────────────────────────────────────────────

def login_student(username, password):
    student = _find_student(username)
    if student and check_password(password, student.password):
        return student
    return None


def login_admin(username, password):
    for a in load_admins():
        if a.username == username and check_password(password, a.password):
            return a
    return None


def register_student(name, username, password):
    students = load_students()
    for s in students:
        if s.username == username:
            return None, "Username already exists."
    existing_nums = [int(s.student_id[1:]) for s in students if s.student_id[1:].isdigit()]
    next_num = max(existing_nums, default=0) + 1
    new_id = f"S{str(next_num).zfill(3)}"
    student = Student(new_id, name, username, password)
    students.append(student)
    save_students(students)
    return student, "Registration successful."


# ── Student operations ─────────────────────────────────────────────────────────

def register_for_course(student_username, course_id):
    students = load_students()
    courses = load_courses()

    student = next((s for s in students if s.username == student_username), None)
    course = next((c for c in courses if c.course_id == course_id), None)

    if not course:
        return False, "Course not found."
    if course_id in student.enrolled_courses:
        return False, "You are already enrolled in this course."
    if not course.is_available():
        return False, "Course is full. No available spots."
    if len(student.enrolled_courses) >= Student.MAX_COURSES:
        return False, f"You cannot enroll in more than {Student.MAX_COURSES} courses."

    student.enrolled_courses.append(course_id)
    course.enrolled_count += 1
    save_students(students)
    save_courses(courses)
    return True, f"Successfully enrolled in [{course.code}] {course.name}."


def drop_course(student_username, course_id):
    students = load_students()
    courses = load_courses()

    student = next((s for s in students if s.username == student_username), None)
    course = next((c for c in courses if c.course_id == course_id), None)

    if not course:
        return False, "Course not found."
    if course_id not in student.enrolled_courses:
        return False, "You are not enrolled in this course."

    student.enrolled_courses.remove(course_id)
    course.enrolled_count = max(0, course.enrolled_count - 1)
    save_students(students)
    save_courses(courses)
    return True, f"Successfully dropped [{course.code}] {course.name}."


def view_my_courses(student_username):
    student = _find_student(student_username)
    courses = load_courses()
    enrolled = [c for c in courses if c.course_id in student.enrolled_courses]
    return enrolled


def view_all_courses():
    return load_courses()


def search_courses(keyword):
    keyword = keyword.lower()
    return [
        c for c in load_courses()
        if keyword in c.name.lower() or keyword in c.code.lower()
    ]


# ── Admin operations ───────────────────────────────────────────────────────────

def add_course(name, code, capacity):
    courses = load_courses()
    for c in courses:
        if c.code.lower() == code.lower():
            return None, "A course with this code already exists."
    existing_nums = [int(c.course_id[1:]) for c in courses if c.course_id[1:].isdigit()]
    next_num = max(existing_nums, default=0) + 1
    new_id = f"C{str(next_num).zfill(3)}"
    course = Course(new_id, name, code, int(capacity))
    courses.append(course)
    save_courses(courses)
    return course, f"Course [{code}] {name} added successfully."


def remove_course(course_id):
    courses = load_courses()
    course = next((c for c in courses if c.course_id == course_id), None)
    if not course:
        return False, "Course not found."

    # Remove from all enrolled students
    students = load_students()
    for s in students:
        if course_id in s.enrolled_courses:
            s.enrolled_courses.remove(course_id)
    save_students(students)

    courses = [c for c in courses if c.course_id != course_id]
    save_courses(courses)
    return True, f"Course [{course.code}] {course.name} removed successfully."


def view_all_students():
    return load_students()
def register_course(student, course_id, storage):
    """Register a student for a course with full validation."""
    course = storage.get_course(course_id)
    if course is None:
        return False, f"Course '{course_id}' does not exist."
    if student.is_registered(course_id):
        return False, f"You are already registered for '{course.name}'."
    if course.is_full():
        return False, f"'{course.name}' is full. No available seats."
    if student.has_reached_limit():
        return False, f"You have reached the maximum limit of {student.MAX_COURSES} courses."

    student.registered_courses.append(course_id)
    course.enrolled_count += 1
    return True, f"Successfully registered for '{course.name}'."


def drop_course(student, course_id, storage):
    """Drop a course the student is registered in."""
    if not student.is_registered(course_id):
        return False, f"You are not registered for course '{course_id}'."
    course = storage.get_course(course_id)
    student.registered_courses.remove(course_id)
    if course is not None:
        course.enrolled_count -= 1
        return True, f"Successfully dropped '{course.name}'."
    return True, f"Successfully dropped course '{course_id}'."


def view_my_courses(student, storage):
    """Return a list of Course objects the student is enrolled in."""
    courses = []
    for cid in student.registered_courses:
        course = storage.get_course(cid)
        if course is not None:
            courses.append(course)
    return courses


def view_all_courses(storage):
    """Return all available courses."""
    return storage.all_courses()


def search_course(keyword, storage):
    """Search courses by course_id, name, or instructor (case-insensitive)."""
    keyword_lower = keyword.lower()
    results = []
    for course in storage.all_courses():
        if (keyword_lower in course.course_id.lower()
                or keyword_lower in course.name.lower()
                or keyword_lower in course.instructor.lower()):
            results.append(course)
    return results
