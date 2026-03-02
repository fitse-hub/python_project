from storage import Storage
from operations import (
    register_course,
    drop_course,
    view_my_courses,
    view_all_courses,
    search_course,
)


def print_separator():
    print("-" * 55)


def print_courses(courses):
    if not courses:
        print("  No courses found.")
        return
    for course in courses:
        print(f"  {course}")


def login(storage):
    """Prompt for student ID and password; return Student on success or None."""
    print_separator()
    print("        STUDENT LOGIN")
    print_separator()
    student_id = input("Enter Student ID: ").strip()
    password = input("Enter Password   : ").strip()
    student = storage.get_student_by_id(student_id)
    if student and student.password == password:
        print(f"\nWelcome, {student.name}!")
        return student
    print("\nInvalid Student ID or password. Please try again.")
    return None


def student_menu(student, storage):
    """Display the student menu and handle choices until logout."""
    while True:
        print_separator()
        print(f"  Student Menu  |  {student.name} ({student.student_id})")
        print_separator()
        print("  1. Register for a course")
        print("  2. Drop a course")
        print("  3. View my courses")
        print("  4. View all available courses")
        print("  5. Search for a course")
        print("  6. Logout")
        print_separator()
        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            print_separator()
            print("  REGISTER FOR A COURSE")
            print_separator()
            print("  Available courses:")
            print_courses(view_all_courses(storage))
            print_separator()
            course_id = input("Enter Course ID to register: ").strip().upper()
            success, message = register_course(student, course_id, storage)
            print(f"\n  {'✔' if success else '✘'} {message}")

        elif choice == "2":
            print_separator()
            print("  DROP A COURSE")
            print_separator()
            my_courses = view_my_courses(student, storage)
            if not my_courses:
                print("  You have no courses to drop.")
            else:
                print("  Your registered courses:")
                print_courses(my_courses)
                print_separator()
                course_id = input("Enter Course ID to drop: ").strip().upper()
                success, message = drop_course(student, course_id, storage)
                print(f"\n  {'✔' if success else '✘'} {message}")

        elif choice == "3":
            print_separator()
            print("  MY COURSES")
            print_separator()
            my_courses = view_my_courses(student, storage)
            if not my_courses:
                print("  You are not registered for any courses yet.")
            else:
                print(f"  Enrolled in {len(my_courses)} course(s):")
                print_courses(my_courses)

        elif choice == "4":
            print_separator()
            print("  ALL AVAILABLE COURSES")
            print_separator()
            print_courses(view_all_courses(storage))

        elif choice == "5":
            print_separator()
            print("  SEARCH COURSES")
            print_separator()
            keyword = input("Enter keyword (name, ID, or instructor): ").strip()
            results = search_course(keyword, storage)
            if not results:
                print("  No courses matched your search.")
            else:
                print(f"  Found {len(results)} course(s):")
                print_courses(results)

        elif choice == "6":
            print(f"\n  Goodbye, {student.name}! You have been logged out.")
            break

        else:
            print("  Invalid option. Please enter a number between 1 and 6.")

        input("\n  Press Enter to continue...")


def main():
    storage = Storage()
    print("=" * 55)
    print("   CONSOLE-BASED COURSE REGISTRATION SYSTEM")
    print("=" * 55)

    while True:
        student = login(storage)
        if student:
            student_menu(student, storage)
        retry = input("\nReturn to login? (y/n): ").strip().lower()
        if retry != "y":
            print("\nThank you for using the Course Registration System. Goodbye!")
            break


if __name__ == "__main__":
    main()
