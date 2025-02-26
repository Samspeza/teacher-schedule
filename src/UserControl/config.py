import sqlite3
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'DbContext')))
from database import DB_NAME

def get_classes():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM classes")
    classes = cursor.fetchall()
    conn.close()
    return [class_[0] for class_ in classes]

def get_teacher_data():
    teachers_data = {}
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM teachers")
    teachers = cursor.fetchall()

    for teacher_id, teacher_name in teachers:
        cursor.execute("""
        SELECT day FROM teacher_availability WHERE teacher_id = ?
        """, (teacher_id,))
        availability = [row[0] for row in cursor.fetchall()]
        teachers_data[teacher_name] = availability

    conn.close()
    return teachers_data

def get_teacher_limits():
    teacher_limits = {}
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT t.name, tl.max_days 
    FROM teachers t
    LEFT JOIN teacher_limits tl ON t.id = tl.teacher_id
    """)
    limits = cursor.fetchall()

    for teacher_name, max_days in limits:
        teacher_limits[teacher_name] = max_days if max_days is not None else 0

    conn.close()
    return teacher_limits

def get_teacher_availability_for_timetable(teacher_limits, teachers_data):
    availability_per_teacher = {}

    for teacher, availability in teachers_data.items():
        max_days = teacher_limits.get(teacher, 0)

        if max_days == 0:
            availability_per_teacher[teacher] = set(availability)  
        else:
            available_days = set(availability[:max_days])  
            availability_per_teacher[teacher] = available_days

    return availability_per_teacher



days_of_week = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]

time_slots = [
    "19:10 - 20:25",  # 1ª aula
    "20:25 - 20:45",  # Intervalo
    "20:45 - 22:00"   # 2ª aula
]

classes = get_classes()
teachers = get_teacher_data()
teacher_limits = get_teacher_limits()

availability_per_teacher = get_teacher_availability_for_timetable(teacher_limits, teachers)

if __name__ == "__main__":
    print("Classes:", classes)
    print("Teachers:", teachers)
    print("Teacher Limits:", teacher_limits)
    print("Teacher Availability:", availability_per_teacher)
