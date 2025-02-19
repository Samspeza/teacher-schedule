import sqlite3
conn = sqlite3.connect('schedule.db')
cursor = conn.cursor()

# Consultar informações sobre a tabela
cursor.execute("PRAGMA table_info(teacher_availability);") # Mudar chamada conforme necessidade
columns = cursor.fetchall()

for column in columns:
    print(column)
conn.close()
