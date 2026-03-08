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
