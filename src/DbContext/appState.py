import sqlite3

class AppState:
    def __init__(self):
        self.db_name = "schedule.db"

    def get_teachers(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, coordinator_id FROM teachers")
        teachers = cursor.fetchall()
        conn.close()
        print(teachers)
        return teachers
        
app_state = AppState()  
