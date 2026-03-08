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
