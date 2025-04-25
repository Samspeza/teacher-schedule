import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class ManageTeachersApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Professores")
        self.root.geometry("800x500")

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True)

        self.tab_dados = ttk.Frame(notebook)
        self.tab_endereco = ttk.Frame(notebook)
        self.tab_perfil = ttk.Frame(notebook)

        notebook.add(self.tab_dados, text="Dados Cadastrais")
        notebook.add(self.tab_endereco, text="Endereço")
        notebook.add(self.tab_perfil, text="Perfil")

        self.setup_dados_tab()

    def setup_dados_tab(self):
        frame = tk.Frame(self.tab_dados, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        labels = [
            "Nome:", "E-mail:", "Telefone:", "Celular:",
            "CPF:", "RG:", "Sexo:", "Data Nasc:",
            "Máx. Dias:", "Disponibilidade:"
        ]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(frame, text=label, anchor="w").grid(row=i, column=0, sticky="w", pady=5)
            if label == "Sexo:":
                sex_combo = ttk.Combobox(frame, values=["Masculino", "Feminino", "Outro"])
                sex_combo.grid(row=i, column=1, sticky="ew", pady=5)
                self.entries[label] = sex_combo
            elif label == "Disponibilidade:":
                days = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
                day_vars = {day: tk.BooleanVar() for day in days}
                self.entries[label] = day_vars
                day_frame = tk.Frame(frame)
                day_frame.grid(row=i, column=1, sticky="w")
                for day, var in day_vars.items():
                    tk.Checkbutton(day_frame, text=day, variable=var).pack(side="left")
            else:
                entry = tk.Entry(frame)
                entry.grid(row=i, column=1, sticky="ew", pady=5)
                self.entries[label] = entry

        # Botões
        btn_frame = tk.Frame(self.tab_dados, pady=10)
        btn_frame.pack()
        tk.Button(btn_frame, text="Salvar", command=self.salvar_professor).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cancelar", command=self.root.quit).pack(side="left", padx=10)

    def salvar_professor(self):
        nome = self.entries["Nome:"].get()
        if not nome:
            messagebox.showerror("Erro", "Nome é obrigatório")
            return

        disponibilidade = [day for day, var in self.entries["Disponibilidade:"].items() if var.get()]
        print("Salvo:", nome, "Disponível:", disponibilidade)
        messagebox.showinfo("Sucesso", "Professor salvo com sucesso!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TeacherFormApp(root)
    root.mainloop()
