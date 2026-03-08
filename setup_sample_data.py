#!/usr/bin/env python3
"""Setup script to populate the system with sample data."""

import models
from operations import add_student, add_course
from storage import save_data

def setup_sample_data():
    print("=" * 60)
    print("SETTING UP SAMPLE DATA")
    print("=" * 60)
    
    # Add courses
    print("\nAdding courses...")
    courses_to_add = [
        ("CS101", "Introduction to Programming", "30"),
        ("CS102", "Data Structures", "25"),
        ("CS103", "Algorithms", "20"),
        ("CS104", "Database Systems", "15"),
        ("CS105", "Web Development", "25"),
    ]
    
    for course_id, name, capacity in courses_to_add:
        success, msg = add_course(course_id, name, capacity)
        print(f"  {'✔' if success else '✘'} {msg}")
    
    # Add students
    print("\nAdding students...")
    students_to_add = [
        ("S001", "Alice Johnson", "password123"),
        ("S002", "Bob Smith", "password123"),
        ("S003", "Carol Williams", "password123"),
    ]
    
    for student_id, name, password in students_to_add:
        success, msg = add_student(student_id, name, password)
        print(f"  {'✔' if success else '✘'} {msg}")
    
    # Save data
    print("\nSaving data...")
    success, msg = save_data(models.users, models.students, models.courses)
    print(f"  {'✔' if success else '✘'} {msg}")
    
    print("\n" + "=" * 60)
    print("SAMPLE DATA SETUP COMPLETE!")
    print("=" * 60)
    print("\nYou can now login as:")
    print("  Admin: username='admin', password='admin123'")
    print("  Student 1: username='S001', password='password123'")
    print("  Student 2: username='S002', password='password123'")
    print("  Student 3: username='S003', password='password123'")
    print("\nRun: python main.py")
    print("=" * 60)

if __name__ == "__main__":
    setup_sample_data()
