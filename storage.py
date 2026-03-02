# storage.py - JSON persistence for the Course Registration System

import json
import os

DATA_FILE = "data.json"


def save_data(users, students, courses):
    """Persist users, students, and courses to a JSON file."""
    data = {
        "users": users,
        "students": students,
        "courses": courses
    }
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True, f"Data saved to '{DATA_FILE}'."
    except (OSError, IOError) as e:
        return False, f"Failed to save data: {e}"


def load_data():
    """Load users, students, and courses from a JSON file.

    Returns a tuple (users, students, courses) with loaded data,
    or (None, None, None) if the file does not exist or is invalid.
    """
    if not os.path.exists(DATA_FILE):
        return None, None, None
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        users = data.get("users", {})
        students = data.get("students", {})
        courses = data.get("courses", {})
        # Ensure list fields are actually lists (safe-guard against corruption)
        for s in students.values():
            s["registered_courses"] = list(s.get("registered_courses", []))
        for c in courses.values():
            c["enrolled_students"] = list(c.get("enrolled_students", []))
        return users, students, courses
    except (json.JSONDecodeError, KeyError, OSError) as e:
        print(f"Warning: Could not load data file – {e}. Starting fresh.")
        return None, None, None
