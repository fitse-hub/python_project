============================================================
  COURSE REGISTRATION SYSTEM
  Console-Based Python Application
============================================================

DESCRIPTION
-----------
A terminal-based Course Registration System that manages
student accounts, course records, enrollment, and reporting
with role-based access control (Admin / Student).

FILE STRUCTURE
--------------
  main.py        – Entry point; menus and authentication
  models.py      – Shared data structures
  operations.py  – Business logic (add, enroll, drop, report)
  storage.py     – JSON persistence (save / load)
  README.txt     – This file

HOW TO RUN
----------
  python main.py

DEFAULT ADMIN CREDENTIALS
--------------------------
  Username : admin
  Password : admin123

FEATURES
--------
  Admin
    • Add new student (creates login account + student record)
    • Add new course with capacity
    • View all students
    • View all courses (with remaining seats)
    • View full enrollment report (per course & per student)
    • Search course by ID or name
    • Logout

  Student
    • Register for a course (validated: capacity, duplicate, max limit)
    • Drop a course
    • View enrolled courses
    • View all available courses
    • Search course by ID or name
    • Logout

VALIDATION RULES
----------------
  • Unique student IDs and course IDs
  • No duplicate enrollment
  • Course capacity enforced
  • Max 5 courses per student
  • Login attempts limited to 3
  • Data persisted to data.json on exit (optional)

TESTING SCENARIOS
-----------------
  Duplicate enrollment  → Error message shown
  Full course           → Registration denied
  Wrong password        → Access denied (3 attempts max)
  Drop non-enrolled     → Error message shown
  Max course limit      → 6th registration denied
