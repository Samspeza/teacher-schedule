import tkinter as tk
import sqlite3
from tkinter import messagebox
from models import get_teachers, get_teacher_availability, insert_teacher

class GradeEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Grade Editor")
        self.geometry("600x400")
        self.create_widgets()
    
    def create_widgets(self):
        self.teacher_list = get_teachers()

        self.tree = tk.Listbox(self)
        for teacher in self.teacher_list:
            self.tree.insert(tk.END, teacher[1])  
        self.tree.pack()

        self.edit_button = tk.Button(self, text="Editar", command=self.edit_teacher)
        self.edit_button.pack()

    def edit_teacher(self):
        selected_teacher_index = self.tree.curselection()
        if not selected_teacher_index:
            messagebox.showerror("Erro", "Selecione um professor para editar.")
            return

        teacher_id = self.teacher_list[selected_teacher_index[0]][0]
        availability = get_teacher_availability(teacher_id)

        edit_window = tk.Toplevel(self)
        edit_window.title("Editar Disponibilidade")

        self.day_vars = {}
        for day in ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"]:
            var = tk.BooleanVar(value=day in availability)
            self.day_vars[day] = var
            tk.Checkbutton(edit_window, text=day, variable=var).pack()

        save_button = tk.Button(edit_window, text="Salvar", command=lambda: self.save_availability(teacher_id))
        save_button.pack()

    def save_availability(self, teacher_id):
        available_days = [day for day, var in self.day_vars.items() if var.get()]
    
        self.update_teacher_availability(teacher_id, available_days)
        messagebox.showinfo("Sucesso", "Disponibilidade salva com sucesso.")
    
    def update_teacher_availability(self, teacher_id, available_days):
        conn = sqlite3.connect("schedule.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM teacher_availability WHERE teacher_id = ?", (teacher_id,))
        for day in available_days:
            cursor.execute("INSERT INTO teacher_availability (teacher_id, day) VALUES (?, ?)", (teacher_id, day))
        
        conn.commit()
        conn.close()

if __name__ == "__main__":
    app = GradeEditor()
    app.mainloop()
