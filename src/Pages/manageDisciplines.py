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
        self.root.geometry("1200x700")
        self.root.configure(bg="#F0F2F5")

        self.sidebar = self.create_sidebar()

        main_frame = tk.Frame(self.root, bg="#F0F2F5")
        main_frame.pack(side="left", fill="both", expand=True)

        header_frame = tk.Frame(main_frame, bg="#F0F2F5", height=70)
        header_frame.pack(fill="x", padx=15, pady=10)

        tk.Label(header_frame, text="📋 Cadastro de Disciplinas", font=("Segoe UI", 16, "bold"),
                 bg="#F8F8F8", fg="#2A72C3").pack(side="left", padx=10)

        filter_frame = tk.Frame(main_frame, bg="#FFFFFF")
        filter_frame.pack(fill="x", padx=15, pady=5)

        self.filter_box = ttk.Combobox(filter_frame, values=["Nome", "Curso"], width=20)
        self.filter_box.set("Nome")
        self.filter_box.pack(side="left", padx=(0, 10))

        self.search_entry = ttk.Entry(filter_frame, width=40)
        self.search_entry.pack(side="left", padx=(0, 5))

        ttk.Button(filter_frame, text="Filtrar", command=self.apply_filter).pack(side="left")

        # Botões principais
        btn_frame = tk.Frame(main_frame, bg="#FFFFFF")
        btn_frame.pack(fill="x", padx=15, pady=5)

        ttk.Button(btn_frame, text="Incluir", command=self.open_discipline_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Editar", command=self.on_update).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.on_delete).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Imprimir", command=lambda: messagebox.showinfo("Imprimir", "Função em construção")).pack(side=tk.LEFT, padx=5)

        # Tabela
        table_frame = tk.Frame(main_frame, bg="#FFFFFF")
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        columns = ("ID", "Curso", "Nome", "Código", "Coordenador")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.pack(fill="both", expand=True)

        # Paginação
        pagination_frame = tk.Frame(main_frame, bg="#F0F2F5")
        pagination_frame.pack(fill="x", pady=(0, 10))

        self.page_num = 1
        self.total_pages = 1
        self.items_per_page = 25

        self.prev_btn = ttk.Button(pagination_frame, text="<<", command=lambda: self.change_page(self.page_num - 1))
        self.prev_btn.pack(side="left", padx=2)

        self.page_label = ttk.Label(pagination_frame, text=f"Página {self.page_num} de {self.total_pages}")
        self.page_label.pack(side="left", padx=10)

        self.next_btn = ttk.Button(pagination_frame, text=">>", command=lambda: self.change_page(self.page_num + 1))
        self.next_btn.pack(side="left", padx=2)

        self.load_disciplines()

    def create_sidebar(self):
        # Sidebar vertical (faixa azul)
        sidebar_frame = tk.Frame(self.root, bg="#007BBD", width=100, height=700)
        sidebar_frame.pack(side="left", fill="y")

        # Ícone de chapéu 🎓 dentro da faixa azul
        self.icon_label = tk.Label(sidebar_frame, text="🎓", font=("Arial", 40), bg="#007BBD", fg="#FFFFFF", cursor="hand2")
        self.icon_label.pack(side="top", padx=20, pady=20)
        self.icon_label.bind("<Button-1>", self.show_home_screen)  

        return sidebar_frame

    def show_home_screen(self, event=None):
        """Retorna à tela inicial."""
        from ScreenManager import ScreenManager
        self.root.destroy()
        home_root = tk.Tk()
        app = ScreenManager(home_root, self.coordinator_id)
        home_root.mainloop()

    def apply_filter(self):
        """Aplica o filtro selecionado na consulta de disciplinas."""
        self.page_num = 1 
        self.load_disciplines()

    def load_disciplines(self):
        """Carrega as disciplinas com base no filtro e página atual."""
        filter_text = self.search_entry.get().lower()
        filter_column = self.filter_box.get().lower()

        where_clause = "WHERE d.coordinator_id = ?"
        params = [self.coordinator_id] 

        if filter_text:
            where_clause += f" AND LOWER(d.{filter_column}) LIKE ?"
            params.append(f'%{filter_text}%')

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT COUNT(*) FROM disciplines d
            LEFT JOIN coordinators c ON d.coordinator_id = c.id
            {where_clause}
        """, params)
        total_items = cursor.fetchone()[0]
        conn.close()

        self.total_pages = (total_items // self.items_per_page) + (1 if total_items % self.items_per_page else 0)

        self.page_label.config(text=f"Página {self.page_num} de {self.total_pages}")

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT DISTINCT d.id, d.course, d.sigla, d.name, d.hours, d.type, d.class_number, c.name AS coordinator_name
            FROM disciplines d
            LEFT JOIN coordinators c ON d.coordinator_id = c.id
            {where_clause}
            LIMIT ? OFFSET ?
        """, params + [self.items_per_page, (self.page_num - 1) * self.items_per_page]) 
        disciplines = cursor.fetchall()
        conn.close()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for discipline in disciplines:
            discipline_id, course, sigla, name, hours, type, class_number, coordinator_name = discipline
            self.tree.insert("", "end", values=(discipline_id, course, name, sigla, coordinator_name))

    def change_page(self, page_num):
        """Altera a página da tabela."""
        if 1 <= page_num <= self.total_pages:
            self.page_num = page_num
            self.load_disciplines()

    def open_discipline_form(self):
        form = tk.Toplevel(self.root)
        form.title("Adicionar Disciplina")
        form.geometry("350x450")
        form.configure(bg="#FFFFFF")

        fields = {
            "Curso": tk.Entry(form),
            "Nome": tk.Entry(form),
            "Sigla (Código)": tk.Entry(form),
            "Horas": tk.Entry(form),
            "Tipo": tk.Entry(form),
            "Número da Turma": tk.Entry(form),
        }

        for label_text, entry in fields.items():
            tk.Label(form, text=label_text, bg="#FFFFFF", anchor="w").pack(fill="x", padx=20, pady=(10, 0))
            entry.pack(fill="x", padx=20)

        def save_discipline():
            try:
                course = fields["Curso"].get()
                name = fields["Nome"].get()
                sigla = fields["Sigla (Código)"].get()
                hours = float(fields["Horas"].get())
                type_value = fields["Tipo"].get()
                class_number = int(fields["Número da Turma"].get())

                if not all([course, name, sigla, hours, type_value, class_number]):
                    raise ValueError("Campos obrigatórios não preenchidos")

                self.add_discipline(course, name, sigla, hours, type_value, class_number)
                form.destroy()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        ttk.Button(form, text="Salvar", command=save_discipline).pack(pady=20)

    def change_page(self, page_num):
        """Altera a página da tabela."""
        if 1 <= page_num <= self.total_pages:
            self.page_num = page_num
            self.load_disciplines()

    def open_discipline_form(self):
        form = tk.Toplevel(self.root)
        form.title("Adicionar Disciplina")
        form.geometry("350x450")
        form.configure(bg="#FFFFFF")

        fields = {
            "Curso": tk.Entry(form),
            "Nome": tk.Entry(form),
            "Sigla (Código)": tk.Entry(form),
            "Horas": tk.Entry(form),
            "Tipo": tk.Entry(form),
            "Número da Turma": tk.Entry(form),
        }

        for label_text, entry in fields.items():
            tk.Label(form, text=label_text, bg="#FFFFFF", anchor="w").pack(fill="x", padx=20, pady=(10, 0))
            entry.pack(fill="x", padx=20)

        def save_discipline():
            try:
                course = fields["Curso"].get()
                name = fields["Nome"].get()
                sigla = fields["Sigla (Código)"].get()
                hours = float(fields["Horas"].get())
                type_value = fields["Tipo"].get()
                class_number = int(fields["Número da Turma"].get())

                if not all([course, name, sigla, hours, type_value, class_number]):
                    raise ValueError("Campos obrigatórios não preenchidos")

                self.add_discipline(course, name, sigla, hours, type_value, class_number)
                form.destroy()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        ttk.Button(form, text="Salvar", command=save_discipline).pack(pady=20)

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

    def delete_discipline(self, discipline_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM disciplines WHERE id = ? AND coordinator_id = ?", 
                       (discipline_id, self.coordinator_id))
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
        form.geometry("300x250")
        form.configure(bg="#FFFFFF")

        tk.Label(form, text="Curso:", bg="#FFFFFF").pack()
        course_entry = tk.Entry(form)
        course_entry.pack()
        course_entry.insert(0, course)

        tk.Label(form, text="Nome:", bg="#FFFFFF").pack()
        name_entry = tk.Entry(form)
        name_entry.pack()
        name_entry.insert(0, name)

        tk.Label(form, text="Código:", bg="#FFFFFF").pack()
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

        ttk.Button(form, text="Salvar", command=save_update).pack(pady=20)
