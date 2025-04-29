import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk

class UserProfileApp:
    def __init__(self, root, coordinator_id):
        self.root = root
        self.coordinator_id = coordinator_id
        self.root.title("Perfil do Coordenador")
        self.root.geometry("700x700")
        self.root.configure(bg="#F0F2F5")

        # Estilo
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("TFrame", background="#F0F2F5")
        self.style.configure("Card.TFrame", background="#FFFFFF")
        self.style.configure("TLabel", background="#F0F2F5", foreground="#333333", font=('Segoe UI', 11))
        self.style.configure("Card.TLabel", background="#FFFFFF", foreground="#333333")
        self.style.configure("Accent.TButton", font=('Segoe UI', 12), padding=8, relief="flat",
                             background="#007bff", foreground="white")
        self.style.map("Accent.TButton",
                       background=[('active', '#0056b3')],
                       foreground=[('active', 'white')])

        self.create_widgets()
        self.load_user_data()

    def show_home_screen(self, event=None):
        """Retorna à tela inicial."""
        from ScreenManager import ScreenManager
        self.root.destroy()
        home_root = tk.Tk()
        app = ScreenManager(home_root, self.coordinator_id)
        home_root.mainloop()

    def create_sidebar(self):
    # Sidebar vertical (faixa azul)
        sidebar_frame = tk.Frame(self.root, bg="#007BBD", width=100, height=700)
        sidebar_frame.pack(side="left", fill="y")

        # Ícone de chapéu 🎓 dentro da faixa azul
        self.icon_label = tk.Label(sidebar_frame, text="🎓", font=("Arial", 40), bg="#007BBD", fg="#FFFFFF", cursor="hand2")
        self.icon_label.pack(side="top", padx=20, pady=20)
        self.icon_label.bind("<Button-1>", self.show_home_screen)  

        return sidebar_frame

    def create_widgets(self):
        self.sidebar = self.create_sidebar()
        # Área Principal
        main_frame = tk.Frame(self.root, bg="#F0F2F5")
        main_frame.pack(side="left", fill="both", expand=True)

        # Cabeçalho
        header_frame = tk.Frame(main_frame, bg="#F0F2F5", height=70)
        header_frame.pack(fill="x", padx=15, pady=10)

        tk.Label(header_frame, text="👤 Perfil do Coordenador", font=("Segoe UI", 16, "bold"),
                bg="#F0F2F5", fg="#2A72C3").pack(side="left", padx=10)

        # Conteúdo do Perfil
        profile_card = ttk.Frame(main_frame, padding=20, style='Card.TFrame')
        profile_card.pack(fill=tk.X, pady=10, padx=15)

        # Canvas do círculo
        self.profile_circle = tk.Canvas(profile_card, width=80, height=80, bg="#FFFFFF", highlightthickness=0, bd=0)
        self.profile_circle.pack(pady=10)
        self.profile_circle.create_oval(5, 5, 75, 75, fill="#007bff", outline="")
        self.initials_label = tk.Label(self.profile_circle, font=('Segoe UI', 24, 'bold'),
                                    fg="white", bg="#007bff")
        self.initials_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Informações
        info_frame = ttk.Frame(profile_card, style='Card.TFrame')
        info_frame.pack(pady=5)

        self.name_label = tk.Label(info_frame, font=('Segoe UI', 18, 'bold'), background="#FFFFFF", foreground="#333333")
        self.name_label.pack()

        self.email_label = tk.Label(info_frame, font=('Segoe UI', 12), background="#FFFFFF", foreground="#6c757d")
        self.email_label.pack()

        self.course_label_frame = ttk.Frame(profile_card, style='Card.TFrame')
        self.course_label_frame.pack(pady=5, fill=tk.X, padx=20)
        tk.Label(self.course_label_frame, text="Curso:", font=('Segoe UI', 12, 'bold'), background="#FFFFFF", foreground="#333333", width=10, anchor=tk.W).pack(side=tk.LEFT)
        self.course_value = tk.Label(self.course_label_frame, text="", font=('Segoe UI', 12), background="#FFFFFF", foreground="#6c757d", anchor=tk.W)
        self.course_value.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # AÇÕES
        actions_frame = ttk.Frame(main_frame, padding=20, style='Card.TFrame')
        actions_frame.pack(fill=tk.X, pady=10)

        tk.Label(actions_frame, text="Ações", font=('Segoe UI', 14, 'bold'), background="#FFFFFF", foreground="#333333").pack(pady=(0, 10), anchor=tk.W)

        # Botões lado a lado ocupando o comprimento da tela
        button_frame = ttk.Frame(actions_frame, style='Card.TFrame')
        button_frame.pack(fill=tk.X)

        # Botões lado a lado, cada um ocupando metade da largura
        edit_button = ttk.Button(button_frame, text="Editar Perfil", style="Accent.TButton", command=self.edit_profile)
        edit_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        password_button = ttk.Button(button_frame, text="Alterar Senha", style="Accent.TButton", command=self.change_password)
        password_button.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # Para garantir que as colunas se expandam igualmente
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)


    def load_user_data(self):
        conn = sqlite3.connect('schedule.db')
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT name, email, course FROM coordinators WHERE id = ?", (self.coordinator_id,))
            user_data = cursor.fetchone()

            if user_data:
                name, email, course = user_data
                self.name_label.config(text=name)
                self.email_label.config(text=email)
                self.course_value.config(text=course)
                initials = ''.join([n[0] for n in name.split()[:2]]).upper()
                self.initials_label.config(text=initials)

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar os dados: {str(e)}")
        finally:
            conn.close()

    def edit_profile(self):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Editar Perfil")
        edit_window.geometry("400x350")
        edit_window.resizable(False, False)
        edit_window.config(bg="#F0F2F5")

        main_frame = ttk.Frame(edit_window, padding=20, style='Card.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="Editar Perfil", font=('Segoe UI', 16, 'bold'), background="#FFFFFF", foreground="#333333").pack(pady=(0, 15))

        fields = [("Nome:", "name"), ("Email:", "email"), ("Curso:", "course")]
        self.edit_vars = {}

        for label_text, field_name in fields:
            label_frame = ttk.Frame(main_frame, style='Card.TFrame')
            label_frame.pack(fill=tk.X, pady=8)
            tk.Label(label_frame, text=label_text, font=('Segoe UI', 11), background="#FFFFFF", foreground="#6c757d", width=8, anchor=tk.W).pack(side=tk.LEFT)
            entry = ttk.Entry(label_frame, font=('Segoe UI', 11))
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            entry.insert(0, getattr(self, f"{field_name}_label", self.course_value).cget("text"))
            self.edit_vars[field_name] = entry

        button_frame = ttk.Frame(main_frame, style='Card.TFrame')
        button_frame.pack(fill=tk.X, pady=(15, 0))
        ttk.Button(button_frame, text="Salvar", command=lambda: self.save_profile(edit_window)).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=edit_window.destroy).pack(side=tk.RIGHT, padx=5)

    def change_password(self):
        pass_window = tk.Toplevel(self.root)
        pass_window.title("Alterar Senha")
        pass_window.geometry("400x300")
        pass_window.resizable(False, False)
        pass_window.config(bg="#F0F2F5")

        main_frame = ttk.Frame(pass_window, padding=20, style='Card.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="Alterar Senha", font=('Segoe UI', 16, 'bold'), background="#FFFFFF", foreground="#333333").pack(pady=(0, 15))

        fields = [("Senha Atual:", "current_pass"), ("Nova Senha:", "new_pass"), ("Confirmar Nova Senha:", "confirm_pass")]
        self.pass_vars = {}

        for label_text, field_name in fields:
            label_frame = ttk.Frame(main_frame, style='Card.TFrame')
            label_frame.pack(fill=tk.X, pady=8)
            tk.Label(label_frame, text=label_text, font=('Segoe UI', 11), background="#FFFFFF", foreground="#6c757d", width=15, anchor=tk.W).pack(side=tk.LEFT)
            entry = ttk.Entry(label_frame, show="*", font=('Segoe UI', 11))
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.pass_vars[field_name] = entry

        button_frame = ttk.Frame(main_frame, style='Card.TFrame')
        button_frame.pack(fill=tk.X, pady=(15, 0))
        ttk.Button(button_frame, text="Salvar", command=lambda: self.save_password(
            self.pass_vars["current_pass"].get(),
            self.pass_vars["new_pass"].get(),
            self.pass_vars["confirm_pass"].get(),
            pass_window
        )).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=pass_window.destroy).pack(side=tk.RIGHT, padx=5)

    def save_profile(self, window):
        new_name = self.edit_vars["name"].get()
        new_email = self.edit_vars["email"].get()
        new_course = self.edit_vars["course"].get()

        if not new_name or not new_email:
            messagebox.showwarning("Aviso", "Nome e email são obrigatórios!")
            return

        conn = sqlite3.connect('schedule.db')
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE coordinators
                SET name = ?, email = ?, course = ?
                WHERE id = ?
            """, (new_name, new_email, new_course, self.coordinator_id))
            conn.commit()

            self.name_label.config(text=new_name)
            self.email_label.config(text=new_email)
            self.course_value.config(text=new_course)
            initials = ''.join([n[0] for n in new_name.split()[:2]]).upper()
            self.initials_label.config(text=initials)

            messagebox.showinfo("Sucesso", "Perfil atualizado com sucesso!")
            window.destroy()

        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Email já está em uso por outro coordenador!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar: {str(e)}")
        finally:
            conn.close()

    def save_password(self, current_pass, new_pass, confirm_pass, window):
        if not current_pass or not new_pass or not confirm_pass:
            messagebox.showwarning("Aviso", "Todos os campos são obrigatórios!")
            return
        if new_pass != confirm_pass:
            messagebox.showerror("Erro", "As senhas não coincidem!")
            return

        conn = sqlite3.connect('schedule.db')
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT password FROM coordinators WHERE id = ?", (self.coordinator_id,))
            db_password = cursor.fetchone()[0]

            if current_pass != db_password:
                messagebox.showerror("Erro", "Senha atual incorreta!")
                return

            cursor.execute("UPDATE coordinators SET password = ? WHERE id = ?", (new_pass, self.coordinator_id))
            conn.commit()
            messagebox.showinfo("Sucesso", "Senha alterada com sucesso!")
            window.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar senha: {str(e)}")
        finally:
            conn.close()
