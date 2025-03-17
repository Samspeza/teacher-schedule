# models.py
import sqlite3
import os
from database import DB_NAME

def execute_query(query, params=()):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def clear_teachers():
    execute_query("DELETE FROM teachers")

def clear_classes():
    execute_query("DELETE FROM classes")

def clear_time_slots():
    execute_query("DELETE FROM time_slots")

def clear_availability():
    execute_query("DELETE FROM teacher_availability")

def reset_ids():
    """Reseta os IDs das tabelas para começar do 1 novamente"""
    execute_query("DELETE FROM sqlite_sequence WHERE name='teachers'")
    execute_query("DELETE FROM sqlite_sequence WHERE name='classes'")
    execute_query("DELETE FROM sqlite_sequence WHERE name='time_slots'")
    execute_query("DELETE FROM sqlite_sequence WHERE name='teacher_availability'")

def get_teachers():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT teachers.id, teachers.name, coordinators.name as coordinator_name
    FROM teachers
    LEFT JOIN coordinators ON teachers.coordinator_id = coordinators.id
    """)

    teachers = cursor.fetchall()
    conn.close()

    return teachers

def get_coordinator_by_teacher(teacher_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT coordinators.name, coordinators.course
    FROM coordinators
    JOIN teachers ON coordinators.id = teachers.coordinator_id
    WHERE teachers.id = ?
    """, (teacher_id,))

    coordinator = cursor.fetchone()
    conn.close()

    return coordinator

def delete_grade_by_id(grade_id):
    """Deleta a grade do banco de dados usando o ID."""
    conn = sqlite3.connect('schedule.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM saved_grades WHERE id = ?", (grade_id,))
    conn.commit()
    conn.close()

def get_teacher_availability(teacher_id, coordinator_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT day FROM teacher_availability WHERE teacher_id = ? AND coordinator_id = ?", (teacher_id, coordinator_id))
    availability = cursor.fetchall()

    conn.close()
    return [day[0] for day in availability]

def get_teacher_limit(teacher_id, coordinator_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT max_days FROM teacher_limits WHERE teacher_id = ? AND coordinator_id = ?", (teacher_id, coordinator_id))
    result = cursor.fetchone()

    conn.close()
    if result and result[0] is not None:
        return result[0]
    else:
        return float('inf')

def insert_class(class_name, coordinator_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO classes (name, coordinator_id)
    VALUES (?, ?)
    """, (class_name, coordinator_id))

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

def get_teachers(coordinator_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM teachers WHERE coordinator_id = ?
    """, (coordinator_id,))
    
    teachers = cursor.fetchall()
    conn.close()
    
    return teachers


def get_teacher_availability(teacher_id, coordinator_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT day FROM teacher_availability WHERE teacher_id = ? AND coordinator_id = ?
    """, (teacher_id, coordinator_id))
    
    availability = cursor.fetchall()
    conn.close()
    
    return [day[0] for day in availability]


def update_teacher_availability(teacher_id, day, new_teacher, coordinator_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE teacher_availability
    SET teacher_id = ?
    WHERE teacher_id = ? AND day = ? AND coordinator_id = ?
    """, (new_teacher, teacher_id, day, coordinator_id))

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

def save_grade(name, contents, coordinator_id):
    """Salva a grade no banco de dados e cria um arquivo correspondente."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO saved_grades (name, content, coordinator_id, file_path)
    VALUES (?, ?, ?, ?)
    """, (name, contents, coordinator_id, ""))  
    
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

def get_saved_grades(coordinator_id):
    """Recupera todas as grades salvas filtrando pelo coordenador"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM saved_grades WHERE coordinator_id = ?", (coordinator_id,))
    result = cursor.fetchall()
    conn.close()
    return result

def get_grade_by_name(grade_name, coordinator_id):
    """Recupera a grade salva pelo nome filtrando pelo coordenador"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM saved_grades WHERE name = ? AND coordinator_id = ?", (grade_name, coordinator_id))
    result = cursor.fetchone()
    conn.close()
    return result

def get_grade_by_id(grade_id, coordinator_id):
    """Recupera os detalhes da grade pelo ID, filtrando pelo coordenador"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM saved_grades WHERE id = ? AND coordinator_id = ?", (grade_id, coordinator_id))
    result = cursor.fetchone()
    conn.close()
    return result

def delete_grade_by_name(grade_name, coordinator_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, file_path FROM saved_grades WHERE name = ? AND coordinator_id = ?", (grade_name, coordinator_id))
    grade_data = cursor.fetchone()
    
    if grade_data:
        grade_id, file_path = grade_data
        if os.path.exists(file_path):
            os.remove(file_path)
        
        cursor.execute("DELETE FROM saved_grades WHERE id = ?", (grade_id,))
        conn.commit()
    
    conn.close()


def get_teachers(self, coordinator_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, FROM teachers WHERE coordinator_id = ?", (coordinator_id,))
    
    teachers = cursor.fetchall()
    conn.close()
    return teachers


def get_teacher_availability(self, teacher_id, coordinator_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT day FROM teacher_availability WHERE teacher_id = ? AND coordinator_id = ?", (teacher_id, coordinator_id))
    
    availability = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return ", ".join(availability)

def load_teachers(self, coordinator_id):
    for row in self.tree.get_children():
        self.tree.delete(row)

    for teacher in self.get_teachers():
        teacher_id, name = teacher
        availability = self.get_teacher_availability(teacher_id, coordinator_id)
        self.tree.insert("", "end", values=(teacher_id, name, availability))

def add_teacher(self, name, coordinator_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO teachers (name, coordinator_id) VALUES (?, ?, ?)", (name, coordinator_id))
    conn.commit()
    conn.close()
    self.load_teachers(coordinator_id) 


def update_teacher(self, teacher_id, name, coordinator_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT coordinator_id FROM teachers WHERE id = ?", (teacher_id,))
    result = cursor.fetchone()

    if result and result[0] == coordinator_id:
        cursor.execute("UPDATE teachers SET name = ?, WHERE id = ?", (name, teacher_id))
        conn.commit()
        self.load_teachers(coordinator_id) 
    else:
        print("Você não tem permissão para atualizar este professor.")
    
    conn.close()


def delete_teacher(self, teacher_id, coordinator_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT coordinator_id FROM teachers WHERE id = ?", (teacher_id,))
    result = cursor.fetchone()

    if result and result[0] == coordinator_id:
        cursor.execute("DELETE FROM teachers WHERE id = ?", (teacher_id,))
        conn.commit()
        cursor.execute("DELETE FROM teacher_availability WHERE teacher_id = ? AND coordinator_id = ?", (teacher_id, coordinator_id))
        conn.commit()

        self.load_teachers(coordinator_id)
    else:
        print("Você não tem permissão para excluir este professor.")
    
    conn.close()

def update_teacher_availability(self, teacher_id, availability, coordinator_id):
    """Atualiza a disponibilidade do professor no banco de dados"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM teacher_availability WHERE teacher_id = ? AND coordinator_id = ?", (teacher_id, coordinator_id))

    for day in availability:
        cursor.execute("INSERT INTO teacher_availability (teacher_id, day, coordinator_id) VALUES (?, ?, ?)", (teacher_id, day, coordinator_id))

    conn.commit()
    conn.close()
    self.load_teachers()

def insert_availability(teacher_id, available_days, coordinator_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    for day in available_days:
        cursor.execute("""
            INSERT INTO teacher_availability (teacher_id, day, coordinator_id)
            VALUES (?, ?, ?)
        """, (teacher_id, day, coordinator_id))

    conn.commit()
    conn.close()


def insert_teacher_limit(teacher_id, max_days, coordinator_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO teacher_limits (teacher_id, max_days, coordinator_id)
    VALUES (?, ?, ?)
    """, (teacher_id, max_days, coordinator_id))
    conn.commit()
    conn.close()

def insert_teacher(teacher_name, coordinator_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO teachers (name, coordinator_id)
        VALUES (?, ?)
    """, (teacher_name, coordinator_id))
    conn.commit()
    teacher_id = cursor.lastrowid  
    conn.close()
    return teacher_id

def insert_discipline(course, sigla, name, hours, type_, class_number, coordinator_id):
    """Insere uma nova disciplina na tabela de disciplinas"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO disciplines (course, sigla, name, hours, type, class_number, coordinator_id)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (course, sigla, name, hours, type_, class_number, coordinator_id))

    conn.commit()
    conn.close()