# models.py
import sqlite3
import sys
import os
from tkinter import messagebox

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

def create_tables():
    conn = sqlite3.connect(DB_NAME)  
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        content TEXT NOT NULL,
        file_path TEXT
    )
    """)
    
    conn.commit() 
    conn.close()  

def delete_grade_from_db(grade_name):
    """Remove uma grade do banco de dados"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM grades WHERE name = ?", (grade_name,))
    conn.commit()
    conn.close()

# Funções do banco de dados em SAVED_GRADES
def save_grade(name, contents):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO saved_grades (name, content, file_path)
    VALUES (?, ?, ?)
    """, (name, contents, ""))  
    
    conn.commit()
    
    grade_id = cursor.lastrowid

    file_name = f"grade_{grade_id}.txt"
    file_path = os.path.join(os.getcwd(), "saved_grades", file_name)
    
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    
    with open(file_path, 'w') as file:
        file.write(contents)

    cursor.execute("""
    UPDATE saved_grades
    SET file_path = ?
    WHERE id = ?
    """, (file_path, grade_id))
    
    conn.commit()
    conn.close()


def get_saved_grades():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM saved_grades")
    return cursor.fetchall()

def get_grade_by_name(grade_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM saved_grades WHERE name = ?", (grade_name,))
    return cursor.fetchone()

def delete_grade_by_name(grade_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, file_path FROM saved_grades WHERE name = ?", (grade_name,))
    grade_data = cursor.fetchone()
    
    if grade_data:
        grade_id, file_path = grade_data
        if os.path.exists(file_path):
            os.remove(file_path)
        cursor.execute("DELETE FROM saved_grades WHERE id = ?", (grade_id,))
        conn.commit()
    conn.close()


def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contents TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()
