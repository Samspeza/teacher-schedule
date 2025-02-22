import sqlite3

from database import DB_NAME
conn = sqlite3.connect('schedule.db')
cursor = conn.cursor()

# Consultar informações sobre a tabela
#cursor.execute("PRAGMA table_info(teacher_availability);") # Mudar chamada conforme necessidade
#columns = cursor.fetchall()

def check_saved_grades():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, content, file_path FROM saved_grades")
    saved_grades = cursor.fetchall()
    conn.close()
    for grade in saved_grades:
        print(grade)


#for column in columns:
#    print(column)
conn.close()
