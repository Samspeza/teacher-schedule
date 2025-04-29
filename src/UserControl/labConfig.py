import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class LabConfigApp:
    def __init__(self, master, db_path, coordinator_id):
        self.master = master
        self.master.title("Configuração de Laboratórios")
        self.coordinator_id = coordinator_id
        self.DB_NAME = db_path

        self.tree = ttk.Treeview(master, columns=("turma", "disciplina", "tipo", "alunos", "divisoes", "lab", "configurado"), show='headings')
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.upper())
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.rows_widgets = []

        self.load_disciplinas_praticas()

        save_button = ttk.Button(master, text="Salvar Configurações", command=self.save_all_configs)
        save_button.pack(pady=10)

    def load_disciplinas_praticas(self):
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT d.id, d.name, d.type, d.class_number, c.name, d.requires_laboratory
            FROM disciplines d
            JOIN classes c ON c.id = d.class_number
            WHERE d.requires_laboratory = 1 AND d.coordinator_id = ?
        """, (self.coordinator_id,))
        disciplinas = cursor.fetchall()

        cursor.execute("SELECT name FROM laboratories")
        labs = [row[0] for row in cursor.fetchall()]

        for disc_id, disc_name, tipo, turma_id, turma_nome, _ in disciplinas:
            cursor.execute("SELECT COUNT(*) FROM students WHERE class_id = ?", (turma_id,))
            num_alunos = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*) FROM lab_division_config 
                WHERE discipline_id = ? AND class_id = ? AND coordinator_id = ?
            """, (disc_id, turma_id, self.coordinator_id))
            configurado = cursor.fetchone()[0] > 0

            self.insert_row(disc_id, turma_id, turma_nome, disc_name, tipo, num_alunos, labs, configurado)

        conn.close()

    def insert_row(self, disc_id, turma_id, turma_nome, disc_name, tipo, alunos, labs, configurado):
        row_id = self.tree.insert("", "end", values=(turma_nome, disc_name, tipo, alunos, '', '', '✔️' if configurado else '❌'))
        spinbox = ttk.Spinbox(self.master, from_=1, to=10, width=5)
        combobox = ttk.Combobox(self.master, values=labs, width=15)
        self.tree.set(row_id, column="divisoes", value=spinbox)
        self.tree.set(row_id, column="lab", value=combobox)
        self.rows_widgets.append((row_id, disc_id, turma_id, spinbox, combobox))

    def save_all_configs(self):
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        for row_id, disc_id, turma_id, spinbox, combobox in self.rows_widgets:
            try:
                divs = int(spinbox.get())
                lab = combobox.get()
                if not lab:
                    continue

                cursor.execute("""
                    DELETE FROM lab_division_config
                    WHERE discipline_id = ? AND class_id = ? AND coordinator_id = ?
                """, (disc_id, turma_id, self.coordinator_id))

                for i in range(1, divs + 1):
                    cursor.execute("""
                        INSERT INTO lab_division_config (class_id, discipline_id, division_number, lab_name, coordinator_id)
                        VALUES (?, ?, ?, ?, ?)
                    """, (turma_id, disc_id, i, lab, self.coordinator_id))

                self.tree.set(row_id, column="configurado", value="✔️")

            except Exception as e:
                print(f"Erro ao salvar configuração para disciplina {disc_id}: {e}")

        conn.commit()
        conn.close()
        messagebox.showinfo("Salvo", "Configurações salvas com sucesso!")

# Exemplo de uso:
# root = tk.Tk()
# app = LabConfigApp(root, "caminho_para_o_banco.db", coordinator_id=1)
# root.mainloop()