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
    cursor.execute("SELECT id, name, max_days FROM teachers")
    teachers = cursor.fetchall()
    conn.close()
    return teachers

def get_teacher_availability(teacher_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT day FROM teacher_availability WHERE teacher_id = ?", (teacher_id,))
    availability = cursor.fetchall()
    conn.close()
    return [day[0] for day in availability]

def get_teacher_limit(teacher_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT max_days FROM teacher_limits WHERE teacher_id = ?", (teacher_id,))
    result = cursor.fetchone()
    
    conn.close()
    if result and result[0] is not None:
        return result[0]
    else:
        return float('inf')  

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

def get_teachers(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, max_days FROM teachers")
        teachers = cursor.fetchall()
        conn.close()
        return teachers

def get_teacher_availability(self, teacher_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT day FROM teacher_availability WHERE teacher_id = ?", (teacher_id,))
        availability = [row[0] for row in cursor.fetchall()]
        conn.close()
        return ", ".join(availability)

def load_teachers(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        for teacher in self.get_teachers():
            teacher_id, name, max_days = teacher
            availability = self.get_teacher_availability(teacher_id)
            self.tree.insert("", "end", values=(teacher_id, name, availability, max_days if max_days else "-"))


def add_teacher(self, name, max_days):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO teachers (name, max_days) VALUES (?, ?)", (name, max_days))
        conn.commit()
        conn.close()
        self.load_teachers()

def update_teacher(self, teacher_id, name, max_days):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE teachers SET name = ?, max_days = ? WHERE id = ?", (name, max_days, teacher_id))
        conn.commit()
        conn.close()
        self.load_teachers()

def delete_teacher(self, teacher_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM teachers WHERE id = ?", (teacher_id,))
        conn.commit()
        conn.close()
        self.load_teachers()

def load_teachers(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        for teacher in self.get_teachers():
            teacher_id, name, max_days = teacher
            availability = self.get_teacher_availability(teacher_id)
            self.tree.insert("", "end", values=(teacher_id, name, availability, max_days if max_days else "-"))

def update_teacher_availability(self, teacher_id, availability):
        """Atualiza a disponibilidade do professor no banco de dados"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM teacher_availability WHERE teacher_id = ?", (teacher_id,))
        
        for day in availability:
            cursor.execute("INSERT INTO teacher_availability (teacher_id, day) VALUES (?, ?)", (teacher_id, day))

        conn.commit()
        conn.close()
        self.load_teachers()

def insert_teacher_limit(teacher_id, max_days):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO teacher_limits (teacher_id, max_days)
    VALUES (?, ?)
    """, (teacher_id, max_days))
    conn.commit()
    conn.close()

def insert_discipline(course, sigla, name, hours, type_, class_number):
    """Insere uma nova disciplina na tabela de disciplinas"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO disciplines (course, sigla, name, hours, type, class_number)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (course, sigla, name, hours, type_, class_number))

    conn.commit()
    conn.close()