# Quick Start Guide - Course Registration System

## Getting Started

### Step 1: Run the System
```bash
python main.py
```

### Step 2: Login as Admin (First Time)
- Username: `admin`
- Password: `admin123`

### Step 3: Add Courses (Admin Only)
From the Admin Menu, select option 2 (Add Course):
- Course ID: CS101
- Course Name: Introduction to Programming
- Capacity: 30

Repeat for more courses.

### Step 4: Add Students (Admin Only)
From the Admin Menu, select option 1 (Add Student):
- Student ID: S001
- Student Name: John Doe
- Password: password123

The student can now login with username `S001` and password `password123`.

### Step 5: Logout and Login as Student
- Logout from admin (option 7)
- Login with student credentials (S001 / password123)

### Step 6: Student Features
Now you can access all student features:
1. Register for Course - Enroll in available courses
2. Drop Course - Remove yourself from a course
3. View My Courses - See your enrolled courses
4. View Available Courses - Browse all courses
5. Search Course - Find courses by ID or name
6. Logout

## All Features Are Working! ✅

The system includes all required validations:
- ✅ Prevents duplicate enrollment
- ✅ Enforces course capacity limits
- ✅ Limits students to 5 courses maximum
- ✅ Validates course existence
- ✅ Role-based access control
- ✅ Data persistence (saves to data.json)

## Need Sample Data?

Run the setup script to populate the system with sample data:
```bash
python setup_sample_data.py
```

This will create:
- 5 courses
- 3 students (S001, S002, S003)
- All with password: `password123`
