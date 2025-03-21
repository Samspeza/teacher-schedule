import sqlite3
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'DbContext')))
from database import DB_NAME

def get_coordinator_id_from_db(username, password):
    """Consulta o banco de dados e retorna o ID do coordenador baseado no login"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM coordinators WHERE name = ? AND password = ?
    """, (username, password))
    coordinator_id = cursor.fetchone()
    conn.close()

    if coordinator_id:
        return coordinator_id[0]
    else:
        return None


def get_classes(coordinator_id):
    """Retorna a lista de classes associadas ao coordenador"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM classes WHERE coordinator_id = ?", (coordinator_id,))
    classes = cursor.fetchall()
    conn.close()
    return [class_[0] for class_ in classes]

def get_disciplines(coordinator_id):
    """Retorna a lista de disciplinas associadas ao coordenador, com filtro por coordinator_id"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT course, sigla, name, hours, type, class_number 
        FROM disciplines 
        WHERE coordinator_id = ?
    """, (coordinator_id,))
    disciplines = cursor.fetchall()
    conn.close()

    disciplines_data = []
    for discipline in disciplines:
        discipline_info = {
            "course": discipline[0],
            "sigla": discipline[1],
            "name": discipline[2],
            "hours": discipline[3],
            "type": discipline[4],
            "class_number": discipline[5]
        }
        disciplines_data.append(discipline_info)
    
    return disciplines_data


def get_class_course(class_name, coordinator_id):
    """Retorna o curso associado a uma classe, filtrado pelo coordenador"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT DISTINCT course 
    FROM disciplines 
    WHERE course = ? AND coordinator_id = ?
    """, (class_name, coordinator_id))

    course = cursor.fetchone()
    conn.close()

    return course[0] if course else None


def get_teacher_data(coordinator_id):
    """Retorna os dados de disponibilidade dos professores, filtrados pelo coordenador"""
    teachers_data = {}
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, name 
    FROM teachers 
    WHERE coordinator_id = ?
    """, (coordinator_id,))
    teachers = cursor.fetchall()

    for teacher_id, teacher_name in teachers:
        cursor.execute("""
        SELECT day 
        FROM teacher_availability 
        WHERE teacher_id = ?
        """, (teacher_id,))
        availability = [row[0] for row in cursor.fetchall()]
        teachers_data[teacher_name] = availability

    conn.close()
    return teachers_data

def get_teacher_limits(coordinator_id):
    """Retorna os limites de dias dos professores, filtrados pelo coordenador"""
    teacher_limits = {}
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT t.name, tl.max_days 
    FROM teachers t
    LEFT JOIN teacher_limits tl ON t.id = tl.teacher_id
    WHERE t.coordinator_id = ?
    """, (coordinator_id,))
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

def get_disciplines_for_class(class_name, coordinator_id):
    """Retorna as disciplinas associadas a uma classe, filtradas pelo coordenador"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT d.name 
    FROM disciplines d
    JOIN class_disciplines cd ON d.id = cd.discipline_id
    JOIN classes c ON c.id = cd.class_id
    WHERE c.name = ? AND d.coordinator_id = ?
    """, (class_name, coordinator_id))
    
    disciplines = cursor.fetchall()
    conn.close()

    return [discipline[0] for discipline in disciplines]

def get_teacher_disciplines(coordinator_id):
    """Retorna as disciplinas associadas aos professores, filtradas pelo coordenador"""
    teacher_disciplines = {}
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT t.name, d.name
    FROM teachers t
    JOIN teacher_disciplines td ON t.id = td.teacher_id
    JOIN disciplines d ON td.discipline_id = d.id
    WHERE d.coordinator_id = ?
    """, (coordinator_id,))
    associations = cursor.fetchall()

    for teacher_name, discipline_name in associations:
        if teacher_name not in teacher_disciplines:
            teacher_disciplines[teacher_name] = []
        teacher_disciplines[teacher_name].append(discipline_name)

    conn.close()
    return teacher_disciplines

def get_coordinator_id_from_db(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM coordinators WHERE email = ? AND password = ?
    """, (username, password))
    coordinator_id = cursor.fetchone()
    conn.close()
    
    if coordinator_id:
        return coordinator_id[0] 
    return None

days_of_week = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]

time_slots = [
    "19:10 - 20:25",  # 1ª aula
    "20:25 - 20:45",  # Intervalo
    "20:45 - 22:00"   # 2ª aula
]

coordinator_id = None  

coordinator_id = None

def login(username, password):
    global coordinator_id
    coordinator_id = get_coordinator_id_from_db(username, password)
    if coordinator_id:
        print("Login bem-sucedido!")
        return True
    else:
        print("Falha no login!")
        return False

# Função de login
def login(username, password):
    global coordinator_id
    coordinator_id = get_coordinator_id_from_db(username, password)
    if coordinator_id:
        print("Login bem-sucedido!")
        return True
    else:
        print("Falha no login!")
        return False

classes = get_classes(coordinator_id)
disciplines = get_disciplines(coordinator_id)
teachers = get_teacher_data(coordinator_id)
teacher_limits = get_teacher_limits(coordinator_id)
teacher_disciplines = get_teacher_disciplines(coordinator_id)
availability_per_teacher = get_teacher_availability_for_timetable(teacher_limits, teachers)

print("Classes:", classes)
print("Disciplines:", disciplines)
print("Teachers:", teachers)
print("Teacher Limits:", teacher_limits)
print("Teacher Availability:", availability_per_teacher)
print("Teacher Disciplines:", teacher_disciplines)
