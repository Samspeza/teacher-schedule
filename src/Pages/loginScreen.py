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
from CSS.style import *
from ScreenManager import ScreenManager

class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Login do Coordenador")
        self.root.geometry("400x350")
        self.root.configure(bg="#F8F8F8")
        
        tk.Label(root, text="Login", font=("Arial", 18, "bold"), bg="#F8F8F8").pack(pady=10)
        
        tk.Label(root, text="Email:", bg="#F8F8F8").pack()
        self.email_entry = tk.Entry(root)
        self.email_entry.pack()
        
        tk.Label(root, text="Senha:", bg="#F8F8F8").pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()
        
        self.login_button = tk.Button(root, text="Entrar", command=self.login, bg="#2A72C3", fg="white")
        self.login_button.pack(pady=10)
        
        self.register_button = tk.Button(root, text="Novo Cadastro", command=self.open_register, bg="#4CAF50", fg="white")
        self.register_button.pack(pady=10)
    
    def login(self):
        """Verifica se o coordenador está cadastrado no banco e abre a tela principal."""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not email or not password:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coordinators WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            self.root.destroy()
            main_root = tk.Tk()
            app = ScreenManager(main_root)
            main_root.mainloop()
        else:
            messagebox.showerror("Erro", "Email ou senha incorretos!")
    
    def open_register(self):
        """Abre a janela de cadastro de coordenador."""
        register_window = tk.Toplevel(self.root)
        register_window.title("Cadastro de Coordenador")
        register_window.geometry("400x400")
        register_window.configure(bg="#F8F8F8")
        
        tk.Label(register_window, text="Nome:", bg="#F8F8F8").pack()
        name_entry = tk.Entry(register_window)
        name_entry.pack()
        
        tk.Label(register_window, text="Email:", bg="#F8F8F8").pack()
        email_entry = tk.Entry(register_window)
        email_entry.pack()
        
        tk.Label(register_window, text="Senha:", bg="#F8F8F8").pack()
        password_entry = tk.Entry(register_window, show="*")
        password_entry.pack()
        
        tk.Label(register_window, text="Curso:", bg="#F8F8F8").pack()
        course_entry = tk.Entry(register_window)
        course_entry.pack()
        
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
            cursor.execute("INSERT INTO coordinators (name, email, password, course) VALUES (?, ?, ?, ?)", (name, email, password, course))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Sucesso", "Coordenador cadastrado com sucesso!")
            register_window.destroy()
        
        tk.Button(register_window, text="Cadastrar", command=register, bg="#4CAF50", fg="white").pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginScreen(root)
    root.mainloop()
