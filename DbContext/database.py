import sqlite3

DB_NAME = "schedule.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        max_days INTEGER NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teacher_availability (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER,
        day TEXT NOT NULL,
        FOREIGN KEY (teacher_id) REFERENCES teachers(id)
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
        name TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER,
        class_id INTEGER,
        day TEXT NOT NULL,
        time_slot_id INTEGER,
        FOREIGN KEY (teacher_id) REFERENCES teachers(id),
        FOREIGN KEY (class_id) REFERENCES classes(id),
        FOREIGN KEY (time_slot_id) REFERENCES time_slots(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action TEXT NOT NULL,
        table_name TEXT NOT NULL,
        old_value TEXT,
        new_value TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        user TEXT NOT NULL
    );
    """)

    cursor.execute("PRAGMA table_info(teacher_availability);")
    columns = cursor.fetchall()

    if not any(col[1] == 'time_slot_id' for col in columns):
        cursor.execute("""
        ALTER TABLE teacher_availability
        ADD COLUMN time_slot_id INTEGER;
        """)

    cursor.execute("PRAGMA foreign_keys=off;")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teacher_availability_new (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER,
        day TEXT NOT NULL,
        time_slot_id INTEGER,
        FOREIGN KEY (teacher_id) REFERENCES teachers(id),
        FOREIGN KEY (time_slot_id) REFERENCES time_slots(id)
    );
    """)

    cursor.execute("""
    INSERT INTO teacher_availability_new (id, teacher_id, day, time_slot_id)
    SELECT id, teacher_id, day, NULL FROM teacher_availability;
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        content TEXT NOT NULL,  
        file_path TEXT         
    );
    """)


    cursor.execute("DROP TABLE teacher_availability;")
    cursor.execute("ALTER TABLE teacher_availability_new RENAME TO teacher_availability;")
    cursor.execute("PRAGMA foreign_keys=on;")

    conn.commit()
    conn.close()
