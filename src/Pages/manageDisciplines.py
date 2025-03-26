import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))  
from CSS.style import *
from UserControl.sidebar import create_sidebar
from DbContext.database import DB_NAME

class ManageSubjectsApp:
    def __init__(self, root, coordinator_id):
        self.root = root
        self.coordinator_id = coordinator_id
        self.root.title("Gerenciamento de Disciplinas")
        self.root.geometry("600x400")

        # Configuração da Treeview para exibir as disciplinas
        self.tree = ttk.Treeview(self.root, columns=("ID", "Curso", "Nome", "Código", "Coordenador"), show="headings")

        self.tree.heading("ID", text="ID")
        self.tree.heading("Curso", text="Curso")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Código", text="Código")
        self.tree.heading("Coordenador", text="Coordenador")

        self.tree.column("ID", width=50)
        self.tree.column("Curso", width=150)
        self.tree.column("Nome", width=150)
        self.tree.column("Código", width=100)
        self.tree.column("Coordenador", width=150)

        self.tree.pack(fill=tk.BOTH, expand=True)

        tk.Button(self.root, text="Adicionar", command=self.open_discipline_form).pack(side=tk.LEFT, padx=10)
        tk.Button(self.root, text="Editar", command=self.on_update).pack(side=tk.LEFT, padx=10)
        tk.Button(self.root, text="Excluir", command=self.on_delete).pack(side=tk.LEFT, padx=10)

        self.load_disciplines()

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
            text="Cadastro de Disciplinas",
            font=("Arial", 16, "bold"),
            bg="#F8F8F8",
            fg="#2A72C3",
            cursor="hand2",
            anchor="w"
        )
        title_label.pack(fill="x", padx=10)

    def open_disciplines(self):
        """Abre a tela de gerenciamento de disciplinas"""
        self.root.destroy()
        disciplines_root = tk.Tk()
        disciplines_app = ManageSubjectsApp(disciplines_root, self.coordinator_id)
        disciplines_root.mainloop()
        self.restart_main_screen()

    def restart_main_screen(self):
        """Reabre a tela principal para atualizar as informações"""
        from ScreenManager import ScreenManager
        main_root = tk.Tk()
        app = ScreenManager(main_root, self.coordinator_id)
        main_root.mainloop()

    def get_disciplines(coordinator_id):
        """Retorna a lista de disciplinas associadas ao coordenador, com filtro por coordinator_id"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT course, sigla, name, hours, type, class_number 
            FROM disciplines 
            WHERE coordinator_id = ?
        """, (coordinator_id,))
        disciplines = cursor.fetchall()
        conn.close()

        disciplines_data = []
        for discipline in disciplines:
            discipline_info = {
                "course": discipline[0],
                "sigla": discipline[1],
                "name": discipline[2],
                "hours": discipline[3],
                "type": discipline[4],
                "class_number": discipline[5]
            }
            disciplines_data.append(discipline_info)
        
        return disciplines_data

    def add_discipline(self, course, name, sigla, hours, type_value, class_number):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO disciplines (course, name, sigla, hours, type, class_number, coordinator_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (course, name, sigla, hours, type_value, class_number, self.coordinator_id))

        conn.commit()
        conn.close()
        self.load_disciplines()


    def update_discipline(self, discipline_id, course, name, sigla):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE disciplines
            SET course = ?, name = ?, sigla = ?
            WHERE id = ? AND coordinator_id = ?
        """, (course, name, sigla, discipline_id, self.coordinator_id))

        conn.commit()
        conn.close()
        self.load_disciplines()


    def delete_discipline(self, discipline_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM disciplines WHERE id = ? AND coordinator_id = ?", 
                    (discipline_id, self.coordinator_id))

        conn.commit()
        conn.close()
        self.load_disciplines()

    def load_disciplines(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT DISTINCT d.id, d.course, d.sigla, d.name, d.hours, d.type, d.class_number, c.name AS coordinator_name
            FROM disciplines d
            LEFT JOIN coordinators c ON d.coordinator_id = c.id
            WHERE d.coordinator_id = ?
        """, (self.coordinator_id,))

        disciplines = cursor.fetchall()
        conn.close()

        for discipline in disciplines:
            discipline_id, course, sigla, name, hours, type, class_number, coordinator_name = discipline
            
            self.tree.insert("", "end", values=(discipline_id, course, name, sigla, coordinator_name))

    def open_discipline_form(self):
        form = tk.Toplevel(self.root)
        form.title("Adicionar/Editar Disciplina")
        form.geometry("300x400") 
        
        # Curso
        tk.Label(form, text="Curso:").pack()
        course_entry = tk.Entry(form)
        course_entry.pack()
        
        # Nome
        tk.Label(form, text="Nome:").pack()
        name_entry = tk.Entry(form)
        name_entry.pack()
        
        # Sigla (Código)
        tk.Label(form, text="Sigla (Código):").pack()
        code_entry = tk.Entry(form)
        code_entry.pack()
        
        # Horas
        tk.Label(form, text="Horas:").pack()
        hours_entry = tk.Entry(form)
        hours_entry.pack()

        # Tipo
        tk.Label(form, text="Tipo:").pack()
        type_entry = tk.Entry(form)
        type_entry.pack()

        # Número da Turma
        tk.Label(form, text="Número da Turma:").pack()
        class_number_entry = tk.Entry(form)
        class_number_entry.pack()

        def save_discipline():
            course = course_entry.get()
            name = name_entry.get()
            sigla = code_entry.get()  
            hours = hours_entry.get()
            type_value = type_entry.get()
            class_number = class_number_entry.get()

            if not course or not name or not sigla or not hours or not type_value or not class_number:
                messagebox.showerror("Erro", "Todos os campos são obrigatórios")
                return
            
            try:
                hours = float(hours)
                class_number = int(class_number)
            except ValueError:
                messagebox.showerror("Erro", "Os campos de horas e número da turma devem ser numéricos válidos.")
                return

            self.add_discipline(course, name, sigla, hours, type_value, class_number)
            form.destroy()
        
        # Botão Salvar
        tk.Button(form, text="Salvar", command=save_discipline).pack()

    def on_delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione uma disciplina para excluir")
            return
        
        discipline_id = self.tree.item(selected[0], "values")[0]
        self.delete_discipline(discipline_id)

    def on_update(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione uma disciplina para editar")
            return

        discipline_id = self.tree.item(selected[0], "values")[0]
        course = self.tree.item(selected[0], "values")[1]
        name = self.tree.item(selected[0], "values")[2]
        code = self.tree.item(selected[0], "values")[3]

        form = tk.Toplevel(self.root)
        form.title("Editar Disciplina")
        form.geometry("300x200")

        tk.Label(form, text="Curso:").pack()
        course_entry = tk.Entry(form)
        course_entry.pack()
        course_entry.insert(0, course)

        tk.Label(form, text="Nome:").pack()
        name_entry = tk.Entry(form)
        name_entry.pack()
        name_entry.insert(0, name)

        tk.Label(form, text="Código:").pack()
        code_entry = tk.Entry(form)
        code_entry.pack()
        code_entry.insert(0, code)

        def save_update():
            new_course = course_entry.get()
            new_name = name_entry.get()
            new_code = code_entry.get()

            if not new_course or not new_name or not new_code:
                messagebox.showerror("Erro", "Todos os campos são obrigatórios")
                return
            
            self.update_discipline(discipline_id, new_course, new_name, new_code)
            form.destroy()

        tk.Button(form, text="Salvar", command=save_update).pack()
