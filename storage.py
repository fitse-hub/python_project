from models import Course, Student


class Storage:
    def __init__(self):
        self.courses = {
            "CS101": Course("CS101", "Introduction to Programming", "Dr. Smith", 30),
            "CS201": Course("CS201", "Data Structures", "Dr. Jones", 25),
            "CS301": Course("CS301", "Algorithms", "Dr. Brown", 20),
            "MATH101": Course("MATH101", "Calculus I", "Prof. Lee", 35),
            "MATH201": Course("MATH201", "Linear Algebra", "Prof. Chen", 30),
            "PHY101": Course("PHY101", "Physics I", "Dr. White", 28),
            "ENG101": Course("ENG101", "Technical Writing", "Ms. Davis", 40),
        }

        self.students = {
            "S001": Student("S001", "Alice", "alice123"),
            "S002": Student("S002", "Bob", "bob456"),
            "S003": Student("S003", "Carol", "carol789"),
        }

    def get_course(self, course_id):
        return self.courses.get(course_id)

    def get_student_by_id(self, student_id):
        return self.students.get(student_id)

    def find_student_by_name_and_password(self, name, password):
        for student in self.students.values():
            if student.name.lower() == name.lower() and student.password == password:
                return student
        return None

    def all_courses(self):
        return list(self.courses.values())
