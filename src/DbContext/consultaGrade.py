import sqlite3

from database import DB_NAME
def get_saved_grades():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM saved_grades")
    return cursor.fetchall()

def print_saved_grades():
    saved_grades = get_saved_grades()
    for grade in saved_grades:
        print(f"ID: {grade[0]}, Nome: {grade[1]}, Conteúdo: {grade[2]}, Caminho do arquivo: {grade[3]}")

if __name__ == "__main__":
    print_saved_grades()