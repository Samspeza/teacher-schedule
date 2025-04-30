import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from CSS.style import *
from UserControl.sidebar import create_sidebar
from DbContext.database import DB_NAME

class ManageProfessorsApp:
    def __init__(self, root, coordinator_id):
        self.root = root
        self.coordinator_id = coordinator_id
        self.root.title("Gerenciamento de Professores")
        self.root.geometry("1175x900")
        self.root.configure(bg="#F0F2F5")

        self.sidebar = self.create_sidebar()

        main_frame = tk.Frame(self.root, bg="#F0F2F5")
        main_frame.pack(side="left", fill="both", expand=True)

        header_frame = tk.Frame(main_frame, bg="#F0F2F5", height=70)
        header_frame.pack(fill="x", padx=15, pady=10)

        tk.Label(header_frame, text="👨‍🏫 Cadastro de Professores", font=("Segoe UI", 16, "bold"),
                 bg="#F8F8F8", fg="#2A72C3").pack(side="left", padx=10)

        filter_frame = tk.Frame(main_frame, bg="#FFFFFF")
        filter_frame.pack(fill="x", padx=15, pady=5)

        self.filter_box = ttk.Combobox(filter_frame, values=["Nome"], width=20)
        self.filter_box.set("Nome")
        self.filter_box.pack(side="left", padx=(0, 10))

        self.search_entry = ttk.Entry(filter_frame, width=40)
        self.search_entry.pack(side="left", padx=(0, 5))

        ttk.Button(filter_frame, text="Filtrar", command=self.apply_filter).pack(side="left")

        btn_frame = tk.Frame(main_frame, bg="#FFFFFF")
        btn_frame.pack(fill="x", padx=15, pady=5)

        ttk.Button(btn_frame, text="Incluir", command=self.open_professor_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Editar", command=self.on_update).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.on_delete).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Imprimir", command=lambda: messagebox.showinfo("Imprimir", "Função em construção")).pack(side=tk.LEFT, padx=5)

        table_frame = tk.Frame(main_frame, bg="#FFFFFF")
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        columns = ("ID", "Nome", "Limite de Dias", "Disponibilidade")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200, anchor="center")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.pack(fill="both", expand=True)

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

        self.load_professors()

    def create_sidebar(self):
        sidebar_frame = tk.Frame(self.root, bg="#007BBD", width=100, height=700)
        sidebar_frame.pack(side="left", fill="y")

        self.icon_label = tk.Label(sidebar_frame, text="🎓", font=("Arial", 40), bg="#007BBD", fg="#FFFFFF", cursor="hand2")
        self.icon_label.pack(side="top", padx=20, pady=20)
        self.icon_label.bind("<Button-1>", self.show_home_screen)

        return sidebar_frame

    def show_home_screen(self, event=None):
        from ScreenManager import ScreenManager
        self.root.destroy()
        home_root = tk.Tk()
        app = ScreenManager(home_root, self.coordinator_id)
        home_root.mainloop()

    def apply_filter(self):
        self.page_num = 1
        self.load_professors()

    def load_professors(self):
        filter_text = self.search_entry.get().lower()
        filter_column = self.filter_box.get().lower()

        where_clause = "WHERE t.coordinator_id = ?"
        params = [self.coordinator_id]

        if filter_text:
            where_clause += f" AND LOWER({filter_column}) LIKE ?"
            params.append(f'%{filter_text}%')

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT COUNT(*) 
            FROM teachers t
            {where_clause}
        """, params)
        total_items = cursor.fetchone()[0]
        conn.close()

        self.total_pages = (total_items // self.items_per_page) + (1 if total_items % self.items_per_page else 0)
        self.page_label.config(text=f"Página {self.page_num} de {self.total_pages}")

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT t.id, t.name, tl.max_days, GROUP_CONCAT(ta.day) AS availability
            FROM teachers t
            LEFT JOIN teacher_limits tl ON tl.teacher_id = t.id
            LEFT JOIN teacher_availability ta ON ta.teacher_id = t.id
            {where_clause}
            GROUP BY t.id
            LIMIT ? OFFSET ?
        """, params + [self.items_per_page, (self.page_num - 1) * self.items_per_page])
        professors = cursor.fetchall()
        conn.close()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for professor in professors:
            self.tree.insert("", "end", values=professor)


    def change_page(self, page_num):
        if 1 <= page_num <= self.total_pages:
            self.page_num = page_num
            self.load_professors()

    def open_professor_form(self):
        form = tk.Toplevel(self.root)
        form.title("Adicionar Professor")
        form.geometry("350x350")
        form.configure(bg="#FFFFFF")

        fields = {
            "Nome": tk.Entry(form),
            "Limite de Dias": tk.Entry(form),
            "Disponibilidade": tk.Entry(form),  
        }

        for label_text, entry in fields.items():
            tk.Label(form, text=label_text, bg="#FFFFFF", anchor="w").pack(fill="x", padx=20, pady=(10, 0))
            entry.pack(fill="x", padx=20)

        def save_professor():
            try:
                name = fields["Nome"].get()
                max_days = fields["Limite de Dias"].get()
                availability = fields["Disponibilidade"].get()

                if not all([name, max_days, availability]):
                    raise ValueError("Campos obrigatórios não preenchidos")

                self.add_professor(name, max_days, availability)
                form.destroy()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        ttk.Button(form, text="Salvar", command=save_professor).pack(pady=20)

    def add_professor(self, name, max_days, availability):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO teachers (name, coordinator_id)
            VALUES (?, ?)
        """, (name, self.coordinator_id))
        professor_id = cursor.lastrowid
        conn.commit()

        cursor.execute("""
            INSERT INTO teacher_limits (teacher_id, max_days, coordinator_id)
            VALUES (?, ?, ?)
        """, (professor_id, max_days, self.coordinator_id))

        days = availability.split(",")  
        for day in days:
            cursor.execute("""
                INSERT INTO teacher_availability (teacher_id, day, coordinator_id)
                VALUES (?, ?, ?)
            """, (professor_id, day.strip(), self.coordinator_id))

        conn.commit()
        conn.close()
        self.load_professors()

    def delete_professor(self, professor_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM teacher_availability WHERE teacher_id = ?", (professor_id,))
        cursor.execute("DELETE FROM teacher_limits WHERE teacher_id = ?", (professor_id,))
        cursor.execute("DELETE FROM teachers WHERE id = ?", (professor_id,))
        conn.commit()
        conn.close()
        self.load_professors()

    def update_professor(self, professor_id, name, max_days, availability):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE teachers
            SET name = ?
            WHERE id = ? AND coordinator_id = ?
        """, (name, professor_id, self.coordinator_id))

        cursor.execute("""
            UPDATE teacher_limits
            SET max_days = ?
            WHERE teacher_id = ? AND coordinator_id = ?
        """, (max_days, professor_id, self.coordinator_id))

        cursor.execute("DELETE FROM teacher_availability WHERE teacher_id = ?", (professor_id,))
        days = availability.split(",")
        for day in days:
            cursor.execute("""
                INSERT INTO teacher_availability (teacher_id, day, coordinator_id)
                VALUES (?, ?, ?)
            """, (professor_id, day.strip(), self.coordinator_id))

        conn.commit()
        conn.close()
        self.load_professors()

    def on_delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um professor para excluir")
            return
        professor_id = self.tree.item(selected[0], "values")[0]
        self.delete_professor(professor_id)

    def on_update(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um professor para editar")
            return

        professor_id = self.tree.item(selected[0], "values")[0]
        name = self.tree.item(selected[0], "values")[1]
        max_days = self.tree.item(selected[0], "values")[2]
        availability = self.tree.item(selected[0], "values")[3]

        form = tk.Toplevel(self.root)
        form.title("Editar Professor")
        form.geometry("350x350")
        form.configure(bg="#FFFFFF")

        tk.Label(form, text="Nome:", bg="#FFFFFF").pack()
        name_entry = tk.Entry(form)
        name_entry.pack()
        name_entry.insert(0, name)

        tk.Label(form, text="Limite de Dias:", bg="#FFFFFF").pack()
        max_days_entry = tk.Entry(form)
        max_days_entry.pack()
        max_days_entry.insert(0, max_days)

        tk.Label(form, text="Disponibilidade (dias separados por vírgula):", bg="#FFFFFF").pack()
        availability_entry = tk.Entry(form)
        availability_entry.pack()
        availability_entry.insert(0, availability)

        def save_update():
            new_name = name_entry.get()
            new_max_days = max_days_entry.get()
            new_availability = availability_entry.get()
            if not new_name or not new_max_days or not new_availability:
                messagebox.showerror("Erro", "Todos os campos são obrigatórios")
                return
            self.update_professor(professor_id, new_name, new_max_days, new_availability)
            form.destroy()

        ttk.Button(form, text="Salvar", command=save_update).pack(pady=20)
