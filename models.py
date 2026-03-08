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

    def __init__(self, student_id, name, password):
        self.student_id = student_id
        self.name = name
        self.password = password
        self.registered_courses = []  # list of course_id strings

    def is_registered(self, course_id):
        return course_id in self.registered_courses

    def has_reached_limit(self):
        return len(self.registered_courses) >= self.MAX_COURSES
