from storage import seed_courses
from operations import (
    login_student, login_admin, register_student,
    register_for_course, drop_course,
    view_my_courses, view_all_courses, search_courses,
    add_course, remove_course, view_all_students,
)


def _separator():
    print("-" * 50)


# ── Student menus ──────────────────────────────────────────────────────────────

def student_menu(student):
    while True:
        _separator()
        print(f"  Student Menu  |  Logged in as: {student.name}")
        _separator()
        print("1. Register for a course")
        print("2. Drop a course")
        print("3. View my courses")
        print("4. View all available courses")
        print("5. Search course")
        print("6. Logout")
        _separator()
        choice = input("Select an option: ").strip()

        if choice == "1":
            student_register_course(student)
        elif choice == "2":
            student_drop_course(student)
        elif choice == "3":
            student_view_my_courses(student)
        elif choice == "4":
            student_view_all_courses()
        elif choice == "5":
            student_search_course()
        elif choice == "6":
            print("Logged out successfully.")
            break
        else:
            print("Invalid option. Please try again.")


def student_register_course(student):
    print("\n-- Register for a Course --")
    courses = view_all_courses()
    if not courses:
        print("No courses available.")
        return
    for c in courses:
        print(f"  {c.course_id}: {c}")
    course_id = input("Enter Course ID to register (or 0 to cancel): ").strip()
    if course_id == "0":
        return
    success, message = register_for_course(student.username, course_id)
    print(message)


def student_drop_course(student):
    print("\n-- Drop a Course --")
    enrolled = view_my_courses(student.username)
    if not enrolled:
        print("You are not enrolled in any courses.")
        return
    for c in enrolled:
        print(f"  {c.course_id}: [{c.code}] {c.name}")
    course_id = input("Enter Course ID to drop (or 0 to cancel): ").strip()
    if course_id == "0":
        return
    success, message = drop_course(student.username, course_id)
    print(message)


def student_view_my_courses(student):
    print("\n-- My Enrolled Courses --")
    enrolled = view_my_courses(student.username)
    if not enrolled:
        print("You are not enrolled in any courses.")
    else:
        for i, c in enumerate(enrolled, 1):
            print(f"  {i}. {c}")


def student_view_all_courses():
    print("\n-- All Available Courses --")
    courses = view_all_courses()
    if not courses:
        print("No courses available.")
    else:
        for i, c in enumerate(courses, 1):
            print(f"  {i}. {c}")


def student_search_course():
    print("\n-- Search Course --")
    keyword = input("Enter course name or code to search: ").strip()
    if not keyword:
        print("Please enter a search term.")
        return
    results = search_courses(keyword)
    if not results:
        print("No courses found matching your search.")
    else:
        print(f"Found {len(results)} result(s):")
        for c in results:
            print(f"  {c}")


# ── Admin menus ────────────────────────────────────────────────────────────────

def admin_menu(admin):
    while True:
        _separator()
        print(f"  Admin Menu  |  Logged in as: {admin.name}")
        _separator()
        print("1. Add course")
        print("2. Remove course")
        print("3. View all courses")
        print("4. View all students")
        print("5. Logout")
        _separator()
        choice = input("Select an option: ").strip()

        if choice == "1":
            admin_add_course()
        elif choice == "2":
            admin_remove_course()
        elif choice == "3":
            student_view_all_courses()
        elif choice == "4":
            admin_view_students()
        elif choice == "5":
            print("Logged out successfully.")
            break
        else:
            print("Invalid option. Please try again.")


def admin_add_course():
    print("\n-- Add New Course --")
    name = input("Course name: ").strip()
    code = input("Course code: ").strip()
    capacity_str = input("Capacity: ").strip()
    if not name or not code or not capacity_str:
        print("All fields are required.")
        return
    if not capacity_str.isdigit() or int(capacity_str) <= 0:
        print("Capacity must be a positive number.")
        return
    capacity = int(capacity_str)
    _, message = add_course(name, code, capacity)
    print(message)


def admin_remove_course():
    print("\n-- Remove Course --")
    courses = view_all_courses()
    if not courses:
        print("No courses to remove.")
        return
    for c in courses:
        print(f"  {c.course_id}: [{c.code}] {c.name}")
    course_id = input("Enter Course ID to remove (or 0 to cancel): ").strip()
    if course_id == "0":
        return
    success, message = remove_course(course_id)
    print(message)


def admin_view_students():
    print("\n-- All Students --")
    students = view_all_students()
    if not students:
        print("No students registered.")
    else:
        for s in students:
            print(f"  [{s.student_id}] {s.name} (username: {s.username}) "
                  f"| Enrolled courses: {len(s.enrolled_courses)}")


# ── Main / Login ───────────────────────────────────────────────────────────────

def login_menu():
    while True:
        _separator()
        print("  Course Registration System")
        _separator()
        print("1. Student Login")
        print("2. Student Register")
        print("3. Admin Login")
        print("4. Exit")
        _separator()
        choice = input("Select an option: ").strip()

        if choice == "1":
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            student = login_student(username, password)
            if student:
                print(f"Welcome, {student.name}!")
                student_menu(student)
            else:
                print("Invalid username or password.")

        elif choice == "2":
            name = input("Full name: ").strip()
            username = input("Choose a username: ").strip()
            password = input("Choose a password: ").strip()
            if not name or not username or not password:
                print("All fields are required.")
                continue
            student, message = register_student(name, username, password)
            print(message)
            if student:
                print(f"Welcome, {student.name}! You can now log in.")

        elif choice == "3":
            username = input("Admin Username: ").strip()
            password = input("Admin Password: ").strip()
            admin = login_admin(username, password)
            if admin:
                print(f"Welcome, {admin.name}!")
                admin_menu(admin)
            else:
                print("Invalid admin credentials.")

        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    seed_courses()
    login_menu()
