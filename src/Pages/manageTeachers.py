import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))  
from CSS.style import *
from UserControl.sidebar import create_sidebar
from DbContext.database import DB_NAME

class ManageTeachersApp:
    def __init__(self, root, coordinator_id):
        self.root = root
        self.coordinator_id = coordinator_id
        self.root.title("Gerenciamento de Professores")
        self.root.geometry("600x400")

        self.tree = ttk.Treeview(self.root, columns=("ID", "Nome", "Disponibilidade", "Máx. Dias", "Coordenador"), show="headings")

        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Disponibilidade", text="Disponibilidade")
        self.tree.heading("Máx. Dias", text="Máx. Dias")
        self.tree.heading("Coordenador", text="Coordenador")

        self.tree.column("ID", width=50)
        self.tree.column("Nome", width=150)
        self.tree.column("Disponibilidade", width=100)
        self.tree.column("Máx. Dias", width=100)
        self.tree.column("Coordenador", width=150)

        self.tree.pack(fill=tk.BOTH, expand=True)


        tk.Button(self.root, text="Adicionar", command=self.open_teacher_form).pack(side=tk.LEFT, padx=10)
        tk.Button(self.root, text="Editar", command=self.on_update).pack(side=tk.LEFT, padx=10)
        tk.Button(self.root, text="Excluir", command=self.on_delete).pack(side=tk.LEFT, padx=10)

        self.load_teachers()

    def setup_ui(self):
        self.sidebar_frame = create_sidebar(
            self.main_frame, 
            show_home_screen=self.show_home_screen,
            show_modules_screen=self.show_modules_screen,
            save_changes=self.save_changes
        )
        self.action_frame = tk.Frame(self.main_frame, bg=BACKGROUND_COLOR)
        self.action_frame.pack(pady=10, padx=10, fill="x")

        self.header_frame = tk.Frame(self.main_frame, bg="#F8F8F8")
        self.header_frame.pack(pady=20, fill="x", padx=10)

        title_label = tk.Label(
            self.header_frame,
            text="Cadastros de Professores",
            font=("Arial", 16, "bold"),
            bg="#F8F8F8",
            fg="#2A72C3",
            cursor="hand2",
            anchor="w"
        )
        title_label.pack(fill="x", padx=10)

    def open_teachers(self):
        """Abre a tela de gerenciamento de professores"""
        self.root.destroy()
        teachers_root = tk.Tk()
        teachers_app = ManageTeachersApp(teachers_root, self.coordinator_id)
        teachers_root.mainloop()
        self.restart_main_screen()

    def restart_main_screen(self):
        """Reabre a tela principal para atualizar as informações"""
        from ScreenManager import ScreenManager
        main_root = tk.Tk()
        app = ScreenManager(main_root, self.coordinator_id)
        main_root.mainloop()

    def get_teachers(self, coordinator_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM teachers WHERE coordinator_id = ?", (coordinator_id,))
        teachers = cursor.fetchall()
        conn.close()
        return teachers
    
    def get_teacher_limits(self, teacher_id, coordinator_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT max_days 
            FROM teacher_limits 
            WHERE teacher_id = ? AND coordinator_id = ?
        """, (teacher_id, coordinator_id))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def get_teacher_availability(self, teacher_id, coordinator_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ta.day 
            FROM teacher_availability ta
            JOIN teachers t ON ta.teacher_id = t.id
            WHERE ta.teacher_id = ? AND t.coordinator_id = ?
        """, (teacher_id, coordinator_id))
        availability = [row[0] for row in cursor.fetchall()]
        conn.close()
        return ", ".join(availability)

    def add_teacher(self, name, max_days):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO teachers (name, coordinator_id) VALUES (?, ?)", 
                    (name, self.coordinator_id))
        
        teacher_id = cursor.lastrowid  

        cursor.execute("INSERT INTO teacher_limits (teacher_id, max_days, coordinator_id) VALUES (?, ?, ?)", 
                    (teacher_id, max_days, self.coordinator_id))

        conn.commit()
        conn.close()
        self.load_teachers()

    def update_teacher(self, teacher_id, name, max_days):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("UPDATE teachers SET name = ? WHERE id = ? AND coordinator_id = ?", 
                    (name, teacher_id, self.coordinator_id))

        cursor.execute("UPDATE teacher_limits SET max_days = ? WHERE teacher_id = ?",
                    (max_days, teacher_id))

        conn.commit()
        conn.close()
        self.load_teachers()

    def delete_teacher(self, teacher_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM teacher_limits WHERE teacher_id = ?", (teacher_id,))

        cursor.execute("DELETE FROM availability WHERE teacher_id = ?", (teacher_id,))

        cursor.execute("DELETE FROM teachers WHERE id = ? AND coordinator_id = ?", 
                    (teacher_id, self.coordinator_id))

        conn.commit()
        conn.close()
        self.load_teachers()

    def load_teachers(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT t.id, t.name, tl.max_days, c.name
            FROM teachers t
            LEFT JOIN teacher_limits tl ON t.id = tl.teacher_id
            LEFT JOIN coordinators c ON tl.coordinator_id = c.id
            WHERE t.coordinator_id = ?
        """, (self.coordinator_id,))

        
        teachers = cursor.fetchall()
        conn.close()

        for teacher in teachers: 
            teacher_id, name, max_days, coordinator_name = teacher
            availability = self.get_teacher_availability(teacher_id, self.coordinator_id)
            self.tree.insert("", "end", values=(teacher_id, name, availability, max_days, coordinator_name))

    def open_teacher_form(self):
        form = tk.Toplevel(self.root)
        form.title("Adicionar/Editar Professor")
        form.geometry("300x200")
        
        tk.Label(form, text="Nome:").pack()
        name_entry = tk.Entry(form)
        name_entry.pack()
        
        tk.Label(form, text="Dias Máximos (Opcional):").pack()
        max_days_entry = tk.Entry(form)
        max_days_entry.pack()
        
        def save_teacher():
            name = name_entry.get()
            max_days = max_days_entry.get() or None
            
            if not name:
                messagebox.showerror("Erro", "O nome do professor é obrigatório")
                return
            
            self.add_teacher(name, max_days)
            form.destroy()
        
        tk.Button(form, text="Salvar", command=save_teacher).pack()

    def on_delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um professor para excluir")
            return
        
        teacher_id = self.tree.item(selected[0], "values")[0]
        self.delete_teacher(teacher_id)

    def on_update(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um professor para editar")
            return

        teacher_id = self.tree.item(selected[0], "values")[0]
        name = self.tree.item(selected[0], "values")[1]
        max_days = self.tree.item(selected[0], "values")[3]
        current_availability = self.get_teacher_availability(teacher_id, self.coordinator_id).split(", ")

        form = tk.Toplevel(self.root)
        form.title("Editar Professor")
        form.geometry("300x300")

        tk.Label(form, text="Nome:").pack()
        name_entry = tk.Entry(form)
        name_entry.pack()
        name_entry.insert(0, name)

        tk.Label(form, text="Dias Máximos (Opcional):").pack()
        max_days_entry = tk.Entry(form)
        max_days_entry.pack()
        if max_days != "-":
            max_days_entry.insert(0, max_days)

        tk.Label(form, text="Disponibilidade:").pack()
        days = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
        day_vars = {day: tk.BooleanVar(value=(day in current_availability)) for day in days}

        for day, var in day_vars.items():
            tk.Checkbutton(form, text=day, variable=var).pack(anchor="w")

        def save_update():
            new_name = name_entry.get()
            new_max_days = max_days_entry.get() or None
            selected_days = [day for day, var in day_vars.items() if var.get()]

            if not new_name:
                messagebox.showerror("Erro", "O nome do professor é obrigatório")
                return
            
            self.update_teacher(teacher_id, new_name, new_max_days)
            self.update_teacher_availability(teacher_id, selected_days)

            form.destroy()

        tk.Button(form, text="Salvar", command=save_update).pack()

    def update_teacher_availability(self, teacher_id, availability):
        """Atualiza a disponibilidade do professor no banco de dados"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM teacher_availability WHERE teacher_id = ? AND teacher_id IN (SELECT id FROM teachers WHERE coordinator_id = ?)", 
                    (teacher_id, self.coordinator_id))

        for day in availability:
            cursor.execute("INSERT INTO teacher_availability (teacher_id, day) VALUES (?, ?)", (teacher_id, day))

        conn.commit()
        conn.close()
        self.load_teachers()
