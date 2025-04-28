import tkinter as tk
from tkinter import messagebox
import sqlite3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'DbContext'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'UserControl'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'CSS'))

from DbContext.database import DB_NAME
from ScreenManager import ScreenManager

class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Teacher Schedule - Login")
        self.root.geometry("800x500")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        # Lado esquerdo - Estilo Suave
        self.left_frame = tk.Frame(root, bg="#6BA8E5", width=400, height=500) 
        self.left_frame.place(x=0, y=0)

        logo = tk.Label(self.left_frame, text="Teacher Schedule", font=("Segoe UI", 22, "bold"),
                        bg="#6BA8E5", fg="white")
        logo.place(x=90, y=40)

        tk.Label(self.left_frame, text="Organize suas grades com facilidade", font=("Segoe UI", 11),
                 bg="#6BA8E5", fg="white").place(x=75, y=80)

        tk.Label(self.left_frame, text="Novo por aqui?", font=("Segoe UI", 14, "bold"),
                 bg="#6BA8E5", fg="white").place(x=130, y=180)

        tk.Label(self.left_frame, text="Crie uma conta de coordenador", font=("Segoe UI", 10),
                 bg="#6BA8E5", fg="white").place(x=105, y=220)

        self.register_button = tk.Button(self.left_frame, text="Cadastrar",
                                         bg="white", fg="#6BA8E5",
                                         font=("Segoe UI", 10, "bold"), relief="flat", bd=0,
                                         command=self.open_register, width=20, height=2,
                                         highlightthickness=0, borderwidth=0,
                                         activebackground="#F5F5F5", activeforeground="#6BA8E5")
        self.register_button.place(x=110, y=270)

        # Lado direito - Login
        self.right_frame = tk.Frame(root, bg="#FFFFFF", width=400, height=500)
        self.right_frame.place(x=400, y=0)

        tk.Label(self.right_frame, text="Bem-vindo de volta!", font=("Segoe UI", 14, "bold"),
                 bg="#FFFFFF", fg="#4A4A4A").place(x=130, y=80)

        tk.Label(self.right_frame, text="Entre com seus dados", font=("Segoe UI", 10),
                 bg="#FFFFFF", fg="gray").place(x=150, y=110)

        self.email_entry = self.create_entry(self.right_frame, "EMAIL", 180)
        self.password_entry = self.create_entry(self.right_frame, "SENHA", 230, show="*")

        self.login_button = tk.Button(self.right_frame, text="ENTRAR", bg="#4A90E2", fg="white",
                                      font=("Segoe UI", 10, "bold"), width=20, height=2,
                                      command=self.login, relief="flat", bd=0,
                                      highlightthickness=0, borderwidth=0,
                                      activebackground="#3E77C0", activeforeground="white")
        self.login_button.place(x=120, y=300)

    def create_entry(self, parent, placeholder, y, show=None):
        label = tk.Label(parent, text=placeholder, font=("Segoe UI", 8), bg="#FFFFFF", anchor='w')
        label.place(x=70, y=y - 20)
        entry = tk.Entry(parent, font=("Segoe UI", 10), width=30, show=show, bd=0, relief="solid",
                         highlightthickness=2, highlightcolor="#A9A9A9", highlightbackground="#D3D3D3", 
                         borderwidth=1)
        entry.place(x=70, y=y)
        entry.config(borderwidth=2, relief="flat", highlightbackground="#D3D3D3")
        return entry

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showerror("Erro", "Preencha todos os campos de login!")
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM coordinators WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            coordinator_id = user[0]
            self.root.destroy()
            main_root = tk.Tk()
            app = ScreenManager(main_root, coordinator_id)
            main_root.mainloop()
        else:
            messagebox.showerror("Erro", "Email ou senha incorretos!")

    def open_register(self):
        register_window = tk.Toplevel(self.root)
        register_window.title("Cadastro de Coordenador")
        register_window.geometry("400x420")
        register_window.configure(bg="#F8F8F8")
        register_window.resizable(False, False)

        # Título
        tk.Label(register_window, text="Cadastro de Coordenador", font=("Segoe UI", 14, "bold"),
                bg="#F8F8F8", fg="#333").pack(pady=20)

        def create_labeled_entry(parent, label_text, show=None):
            frame = tk.Frame(parent, bg="#F8F8F8")
            frame.pack(pady=5)
            tk.Label(frame, text=label_text, bg="#F8F8F8", anchor="w", width=30).pack()
            entry = tk.Entry(frame, font=("Segoe UI", 10), show=show, width=30, bd=0, relief="solid",
                             highlightthickness=2, highlightcolor="#A9A9A9", highlightbackground="#D3D3D3", 
                             borderwidth=1)
            entry.pack()
            entry.config(borderwidth=2, relief="flat", highlightbackground="#D3D3D3")
            return entry

        name_entry = create_labeled_entry(register_window, "Nome:")
        email_entry = create_labeled_entry(register_window, "Email:")
        password_entry = create_labeled_entry(register_window, "Senha:", show="*")
        course_entry = create_labeled_entry(register_window, "Curso:")

        def register():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            password = password_entry.get().strip()
            course = course_entry.get().strip()

            if not name or not email or not password or not course:
                messagebox.showerror("Erro", "Preencha todos os campos!")
                return

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO coordinators (name, email, password, course) VALUES (?, ?, ?, ?)",
                        (name, email, password, course))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Coordenador cadastrado com sucesso!")
            register_window.destroy()

        # Botão de cadastrar
        tk.Button(register_window, text="Cadastrar", command=register,
                bg="#4A90E2", fg="white", font=("Segoe UI", 10, "bold"),
                width=20, height=2, relief="flat", bd=0,
                highlightthickness=0, borderwidth=0,
                activebackground="#3E77C0", activeforeground="white").pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginScreen(root)
    root.mainloop()
