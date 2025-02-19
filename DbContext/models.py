# models.py
import sqlite3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'DbContext')))
from database import DB_NAME

DB_NAME = "schedule.db"

def get_teachers():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM teachers")
    teachers = cursor.fetchall()
    conn.close()
    return teachers

def get_teacher_availability(teacher_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT day
    FROM teacher_availability
    WHERE teacher_id = ?
    """, (teacher_id,))
    availability = cursor.fetchall()
    conn.close()
    return availability


def insert_teacher(name, max_days=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO teachers (name, max_days)
    VALUES (?, ?)
    """, (name, max_days))

    teacher_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return teacher_id

def insert_availability(teacher_id, available_days):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for day in available_days:
        cursor.execute("""
        INSERT INTO teacher_availability (teacher_id, day)
        VALUES (?, ?)
        """, (teacher_id, day))

    conn.commit()
    conn.close()

def insert_class(class_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO classes (name)
    VALUES (?)
    """, (class_name,))

    conn.commit()
    conn.close()

def insert_time_slot(time_range):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO time_slots (time_range)
    VALUES (?)
    """, (time_range,))

    conn.commit()
    conn.close()

def get_teachers():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM teachers
    """)
    
    teachers = cursor.fetchall()
    conn.close()
    
    return teachers

def get_teacher_availability(teacher_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT day FROM teacher_availability WHERE teacher_id = ?
    """, (teacher_id,))
    
    availability = cursor.fetchall()
    conn.close()
    
    return [day[0] for day in availability]

def update_teacher_availability(teacher_id, day, new_teacher):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE teacher_availability
    SET teacher_id = ?
    WHERE teacher_id = ? AND day = ?
    """, (new_teacher, teacher_id, day))

    conn.commit()
    conn.close()

def log_change(action, table_name, old_value, new_value, user):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO logs (action, table_name, old_value, new_value, user)
    VALUES (?, ?, ?, ?, ?)
    """, (action, table_name, old_value, new_value, user))

    conn.commit()
    conn.close()
