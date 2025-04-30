import os
import sqlite3

DB_NAME = "schedule.db"

def create_tables():
    print(f"Banco de dados sendo criado no diretório: {os.getcwd()}")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coordinators (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        course TEXT NOT NULL
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        coordinator_id INTEGER,
        FOREIGN KEY (coordinator_id) REFERENCES coordinators(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS availability (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER NOT NULL,
        available_days TEXT NOT NULL,
        coordinator_id INTEGER NOT NULL,
        FOREIGN KEY (teacher_id) REFERENCES teachers(id),
        FOREIGN KEY (coordinator_id) REFERENCES coordinators(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teacher_availability (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER,
        day TEXT NOT NULL,
        time_slot_id INTEGER,
        coordinator_id INTEGER,
        FOREIGN KEY (teacher_id) REFERENCES teachers(id),
        FOREIGN KEY (time_slot_id) REFERENCES time_slots(id),
        FOREIGN KEY (coordinator_id) REFERENCES coordinators(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS time_slots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time_range TEXT NOT NULL
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        course TEXT NOT NULL,
        student_count INTEGER NOT NULL,
        coordinator_id INTEGER,
        FOREIGN KEY (coordinator_id) REFERENCES coordinators(id)
    );
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER,
        class_id INTEGER,
        day TEXT NOT NULL,
        time_slot_id INTEGER,
        coordinator_id INTEGER,
        FOREIGN KEY (teacher_id) REFERENCES teachers(id),
        FOREIGN KEY (class_id) REFERENCES classes(id),
        FOREIGN KEY (time_slot_id) REFERENCES time_slots(id),
        FOREIGN KEY (coordinator_id) REFERENCES coordinators(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        content TEXT NOT NULL,
        file_path TEXT,
        coordinator_id INTEGER,
        FOREIGN KEY (coordinator_id) REFERENCES coordinators(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teacher_limits (
        teacher_id INTEGER,
        max_days INTEGER, 
        coordinator_id INTEGER,
        FOREIGN KEY (teacher_id) REFERENCES teachers(id),
        FOREIGN KEY (coordinator_id) REFERENCES coordinators(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS laboratories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        available_days TEXT NOT NULL,
        daily_limit INTEGER NOT NULL,
        capacity INTEGER NOT NULL,
        coordinator_id INTEGER,
        FOREIGN KEY (coordinator_id) REFERENCES coordinators(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS disciplines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course TEXT NOT NULL,
        sigla TEXT NOT NULL,
        name TEXT NOT NULL,
        hours REAL NOT NULL,
        type TEXT NOT NULL,
        class_number INTEGER NOT NULL,
        requires_laboratory BOOLEAN NOT NULL DEFAULT FALSE,
        laboratory_id INTEGER DEFAULT NULL,
        coordinator_id INTEGER,
        FOREIGN KEY (coordinator_id) REFERENCES coordinators(id),
        FOREIGN KEY (laboratory_id) REFERENCES laboratories(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teacher_disciplines (
        teacher_id INTEGER,
        discipline_id INTEGER,
        coordinator_id INTEGER,
        FOREIGN KEY (teacher_id) REFERENCES teachers(id),
        FOREIGN KEY (discipline_id) REFERENCES disciplines(id),
        FOREIGN KEY (coordinator_id) REFERENCES coordinators(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS class_divisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        coordinator_id INTEGER NOT NULL,
        class_name TEXT NOT NULL,
        divisions INTEGER NOT NULL DEFAULT 1
    );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lab_division_config (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER NOT NULL,
        discipline_id INTEGER NOT NULL,
        division_number INTEGER NOT NULL,
        lab_id INTEGER NOT NULL,
        coordinator_id INTEGER,
        FOREIGN KEY (class_id) REFERENCES classes(id),
        FOREIGN KEY (discipline_id) REFERENCES disciplines(id),
        FOREIGN KEY (lab_id) REFERENCES laboratories(id),
        FOREIGN KEY (coordinator_id) REFERENCES coordinators(id)
    );

    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS discipline_class (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        discipline_id INTEGER,
        class_id INTEGER,
        FOREIGN KEY (discipline_id) REFERENCES disciplines(id),
        FOREIGN KEY (class_id) REFERENCES classes(id)
    )
    """)
            
    conn.commit()
    conn.close()

