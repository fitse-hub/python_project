# main.py - Entry point for the Course Registration System

import sys
import models
from operations import (
    authenticate,
    add_student,
    add_course,
    view_all_students,
    view_all_courses,
    view_enrollment_reports,
    register_course,
    drop_course,
    view_my_courses,
    search_course,
)
from storage import save_data, load_data

MAX_LOGIN_ATTEMPTS = 3


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def print_header(title):
    width = 60
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def get_input(prompt, allow_empty=False):
    """Prompt for input and strip whitespace. Repeat if empty and not allowed."""
    while True:
        value = input(prompt).strip()
        if value or allow_empty:
            return value
        print("  [!] Input cannot be empty. Please try again.")


def confirm_action(prompt="Are you sure? (y/n): "):
    return get_input(prompt, allow_empty=True).lower() == "y"


# ---------------------------------------------------------------------------
# Admin menu
# ---------------------------------------------------------------------------

def admin_menu(username):
    while True:
        print_header("ADMIN MENU")
        print("  1. Add Student")
        print("  2. Add Course")
        print("  3. View All Students")
        print("  4. View All Courses")
        print("  5. View Enrollment Reports")
        print("  6. Search Course")
        print("  7. Logout")
        print()

        choice = get_input("Enter your choice (1-7): ", allow_empty=True)

        if choice == "1":
            print_header("ADD STUDENT")
            student_id = get_input("  Student ID   : ")
            name = get_input("  Student Name : ")
            password = get_input("  Password     : ")
            success, msg = add_student(student_id, name, password)
            print(f"\n  {'✔' if success else '✘'} {msg}")

        elif choice == "2":
            print_header("ADD COURSE")
            course_id = get_input("  Course ID    : ")
            course_name = get_input("  Course Name  : ")
            capacity = get_input("  Capacity     : ")
            success, msg = add_course(course_id, course_name, capacity)
            print(f"\n  {'✔' if success else '✘'} {msg}")

        elif choice == "3":
            print_header("ALL STUDENTS")
            print(view_all_students())

        elif choice == "4":
            print_header("ALL COURSES")
            print(view_all_courses())

        elif choice == "5":
            print(view_enrollment_reports())

        elif choice == "6":
            print_header("SEARCH COURSE")
            query = get_input("  Enter course ID or name: ")
            print(search_course(query))

        elif choice == "7":
            print("\n  Logging out...\n")
            break

        else:
            print("\n  [!] Invalid choice. Please enter a number between 1 and 7.")


# ---------------------------------------------------------------------------
# Student menu
# ---------------------------------------------------------------------------

def student_menu(username):
    while True:
        print_header(f"STUDENT MENU  ({username})")
        print("  1. Register for Course")
        print("  2. Drop Course")
        print("  3. View My Courses")
        print("  4. View Available Courses")
        print("  5. Search Course")
        print("  6. Logout")
        print()

        choice = get_input("Enter your choice (1-6): ", allow_empty=True)

        if choice == "1":
            print_header("REGISTER FOR COURSE")
            print(view_all_courses())
            print()
            course_id = get_input("  Enter Course ID to register: ")
            success, msg = register_course(username, course_id)
            print(f"\n  {'✔' if success else '✘'} {msg}")

        elif choice == "2":
            print_header("DROP COURSE")
            print(view_my_courses(username))
            print()
            course_id = get_input("  Enter Course ID to drop: ")
            success, msg = drop_course(username, course_id)
            print(f"\n  {'✔' if success else '✘'} {msg}")

        elif choice == "3":
            print_header("MY COURSES")
            print(view_my_courses(username))

        elif choice == "4":
            print_header("AVAILABLE COURSES")
            print(view_all_courses())

        elif choice == "5":
            print_header("SEARCH COURSE")
            query = get_input("  Enter course ID or name: ")
            print(search_course(query))

        elif choice == "6":
            print("\n  Logging out...\n")
            break

        else:
            print("\n  [!] Invalid choice. Please enter a number between 1 and 6.")


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------

def login_screen():
    """Handle login with up to MAX_LOGIN_ATTEMPTS tries. Returns (username, role)."""
    attempts = 0
    while attempts < MAX_LOGIN_ATTEMPTS:
        remaining = MAX_LOGIN_ATTEMPTS - attempts
        if remaining < MAX_LOGIN_ATTEMPTS:
            print(f"\n  [!] {remaining} attempt(s) remaining.")
        username = get_input("  Username : ")
        password = get_input("  Password : ")

        role, msg = authenticate(username, password)
        if role:
            print(f"\n  ✔ {msg} Welcome, {username}! (Role: {role})")
            return username, role
        else:
            print(f"\n  ✘ {msg}")
            attempts += 1

    print("\n  [!] Too many failed attempts. Returning to main menu.\n")
    return None, None


# ---------------------------------------------------------------------------
# Main menu / entry point
# ---------------------------------------------------------------------------

def main():
    print_header("COURSE REGISTRATION SYSTEM")
    print("  Loading data...")

    # Load persisted data if available
    loaded_users, loaded_students, loaded_courses = load_data()
    if loaded_users is not None:
        models.users.clear()
        models.users.update(loaded_users)
        models.students.clear()
        models.students.update(loaded_students)
        models.courses.clear()
        models.courses.update(loaded_courses)
        print("  ✔ Data loaded successfully.")
    else:
        print("  ℹ  No saved data found. Starting with default admin account.")

    while True:
        print_header("MAIN MENU")
        print("  1. Login")
        print("  2. Exit")
        print()

        choice = get_input("Enter your choice (1-2): ", allow_empty=True)

        if choice == "1":
            print_header("LOGIN")
            username, role = login_screen()
            if role == "admin":
                admin_menu(username)
            elif role == "student":
                student_menu(username)

        elif choice == "2":
            if confirm_action("  Save data before exiting? (y/n): "):
                success, msg = save_data(models.users, models.students, models.courses)
                print(f"\n  {'✔' if success else '✘'} {msg}")
            print("\n  Goodbye!\n")
            sys.exit(0)

        else:
            print("\n  [!] Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
