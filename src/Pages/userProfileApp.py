import tkinter as tk
from tkinter import messagebox
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))  
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'DbContext'))
import sqlite3
from DbContext.database import DB_NAME

class UserProfileApp:
    def __init__(self, root, coordinator_id):
        self.root = root
        self.root.title("Perfil do Usuário")
        self.root.geometry("400x400")
        self.coordinator_id = coordinator_id

        tk.Label(root, text="Nome:").pack(pady=5)
        self.name_entry = tk.Entry(root)
        self.name_entry.pack(pady=5)

        tk.Label(root, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(root)
        self.email_entry.pack(pady=5)

        tk.Label(root, text="Curso:").pack(pady=5)
        self.course_entry = tk.Entry(root)
        self.course_entry.pack(pady=5)

        tk.Label(root, text="Nova Senha (deixe em branco para não alterar):").pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(root, text="Salvar Alterações", command=self.save_changes).pack(pady=20)
        tk.Button(root, text="Fechar", command=self.show_home_screen).pack(pady=5) 
        self.load_user_data()


    def show_home_screen(self):
        from ScreenManager import ScreenManager
        """Retorna à tela inicial."""
        self.root.destroy()
        home_root = tk.Tk()
        app = ScreenManager(home_root, self.coordinator_id)
        home_root.mainloop()

    def load_user_data(self):
        """Carrega os dados do usuário do banco de dados."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT name, email, course FROM coordinators WHERE id = ?", (self.coordinator_id,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            self.name, self.email, self.course = user_data
            self.name_entry.insert(0, self.name)
            self.email_entry.insert(0, self.email)
            self.course_entry.insert(0, self.course)
        else:
            messagebox.showerror("Erro", "Usuário não encontrado!")
            self.root.destroy()

    def save_changes(self):
        """Salva as alterações no banco de dados."""
        new_name = self.name_entry.get()
        new_email = self.email_entry.get()
        new_course = self.course_entry.get()
        new_password = self.password_entry.get()

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        if new_password:
            cursor.execute("UPDATE coordinators SET name = ?, email = ?, course = ?, password = ? WHERE id = ?", 
                           (new_name, new_email, new_course, new_password, self.coordinator_id))
        else:
            cursor.execute("UPDATE coordinators SET name = ?, email = ?, course = ? WHERE id = ?", 
                           (new_name, new_email, new_course, self.coordinator_id))

        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")

if __name__ == "__main__":
    root = tk.Tk()
    app = UserProfileApp(root) 
    root.mainloop()
