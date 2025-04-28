import tkinter as tk
from tkinter import ttk
from Pages.manageDisciplines import ManageSubjectsApp
from Pages.saved_grades import SavedGradesApp
from Pages.manageTeachers import ManageProfessorsApp
from Pages.userProfileApp import UserProfileApp

from PIL import Image, ImageTk  # Usando Pillow para exibir a imagem
import io  # Para salvar a imagem em formato de buffer

import tkinter as tk
from tkinter import ttk

class ScreenManager:
    def __init__(self, root, coordinator_id):
        self.root = root
        self.coordinator_id = coordinator_id

        self.root.title("Teacher Schedule Dashboard")
        self.root.geometry("1200x800")
        self.root.configure(bg="#F4F6FA")  # Cor de fundo suave

        # Sidebar
        self.sidebar = tk.Frame(self.root, bg="#FFFFFF", width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.create_sidebar()

        # Topbar
        self.topbar = tk.Frame(self.root, bg="#FFFFFF", height=80)
        self.topbar.pack(side=tk.TOP, fill=tk.X)

        self.create_topbar()

        # Main content area
        self.main_content = tk.Frame(self.root, bg="#F4F6FA")
        self.main_content.pack(expand=True, fill=tk.BOTH)

        self.create_dashboard()

    def create_sidebar(self):
        title = tk.Label(self.sidebar, text="LingLee", font=("Helvetica", 22, "bold"), bg="#FFFFFF", fg="#2A72C3")
        title.pack(pady=(30, 50))

        # Sidebar buttons
        self.create_nav_button("Criar Grade", self.open_timetable)
        self.create_nav_button("Grades Salvas", self.open_saved)
        self.create_nav_button("Gerenciar Professores", self.open_teachers)
        self.create_nav_button("Cadastrar Disciplina", self.open_subjects)

    def create_nav_button(self, text, command):
        button = tk.Button(self.sidebar, text=text, font=("Helvetica", 14), bg="#FFFFFF", fg="#333333",
                           bd=0, relief="flat", activebackground="#EEF1F8", activeforeground="#2A72C3",
                           anchor="w", padx=20, command=command, cursor="hand2")
        button.pack(fill=tk.X, pady=5)

    def create_topbar(self):
        welcome_label = tk.Label(self.topbar, text="Bem-vindo(a) de volta!", font=("Helvetica", 16, "bold"),
                                 bg="#FFFFFF", fg="#2A72C3")
        welcome_label.pack(side=tk.LEFT, padx=30)

        profile_btn = tk.Button(self.topbar, text="Perfil", font=("Helvetica", 12), bg="#2A72C3", fg="white",
                                padx=10, pady=5, bd=0, cursor="hand2", command=self.open_user_profile)
        profile_btn.pack(side=tk.RIGHT, padx=30)

    def create_dashboard(self):
        card = tk.Frame(self.main_content, bg="#FFFFFF", bd=0, relief="solid", 
                        highlightthickness=1, highlightbackground="#E0E0E0", padx=20, pady=20)
        card.place(relx=0.5, rely=0.5, anchor="center", width=800, height=500)

        title = tk.Label(card, text="Teacher Schedule", font=("Helvetica", 24, "bold"), bg="#FFFFFF", fg="#2A72C3")
        title.pack(pady=20)

        subtitle = tk.Label(card, text="Gerencie suas atividades de forma simples", font=("Helvetica", 14),
                            bg="#FFFFFF", fg="#666666")
        subtitle.pack(pady=10)

        button_frame = tk.Frame(card, bg="#FFFFFF")
        button_frame.pack(pady=30)

        self.create_dashboard_button(button_frame, "Criar Grade", self.open_timetable)
        self.create_dashboard_button(button_frame, "Grades Salvas", self.open_saved)
        self.create_dashboard_button(button_frame, "Gerenciar Professores", self.open_teachers)
        self.create_dashboard_button(button_frame, "Cadastrar Disciplina", self.open_subjects)

        # Exibição de informações para o coordenador
        self.create_info_panel()

    def create_dashboard_button(self, parent, text, command):
        button = tk.Button(parent, text=text, font=("Helvetica", 12, "bold"), bg="#2A72C3", fg="white",
                           width=20, height=2, bd=0, relief="flat", cursor="hand2", command=command)
        button.pack(pady=10)

    def create_info_panel(self):
        info_frame = tk.Frame(self.main_content, bg="#FFFFFF", bd=0, relief="solid", 
                              highlightthickness=1, highlightbackground="#E0E0E0", padx=20, pady=20)
        info_frame.place(relx=0.8, rely=0.5, anchor="center", width=300, height=200)

        title = tk.Label(info_frame, text="Informações Relevantes", font=("Helvetica", 16, "bold"), bg="#FFFFFF", fg="#2A72C3")
        title.pack(pady=20)

        info_label = tk.Label(info_frame, text="Revisar grades salvas, controlar a alocação de professores, " 
                                              "e garantir a disponibilidade das disciplinas.",
                              font=("Helvetica", 12), bg="#FFFFFF", fg="#666666")
        info_label.pack(pady=10)

        # Perfil do coordenador
        self.create_coordinator_profile(info_frame)

    def create_coordinator_profile(self, parent):
        profile_frame = tk.Frame(parent, bg="#FFFFFF", bd=0, relief="solid", padx=10, pady=10, 
                                 highlightthickness=1, highlightbackground="#E0E0E0")
        profile_frame.pack(pady=20)

        profile_title = tk.Label(profile_frame, text="Coordenador", font=("Helvetica", 14, "bold"), bg="#FFFFFF", fg="#2A72C3")
        profile_title.pack()

        # Exemplo de dados de coordenador (substituir conforme necessário)
        name_label = tk.Label(profile_frame, text="Nome: João Silva", font=("Helvetica", 12), bg="#FFFFFF", fg="#666666")
        name_label.pack()

        email_label = tk.Label(profile_frame, text="Email: joao.silva@exemplo.com", font=("Helvetica", 12), bg="#FFFFFF", fg="#666666")
        email_label.pack()

    def open_user_profile(self):
        self.root.destroy()
        user_root = tk.Tk()
        user_app = UserProfileApp(user_root, self.coordinator_id)
        user_root.mainloop()

    def open_timetable(self):
        self.root.destroy()
        from Pages.teacherschedule import TimetableApp
        timetable_root = tk.Tk()
        app = TimetableApp(timetable_root, self.coordinator_id)
        timetable_root.mainloop()

    def open_saved(self):
        self.root.destroy()
        saved_root = tk.Tk()
        saved_app = SavedGradesApp(saved_root, self.coordinator_id)
        saved_root.mainloop()

    def open_teachers(self):
        self.root.destroy()
        teachers_root = tk.Tk()
        teachers_app = ManageProfessorsApp(teachers_root, self.coordinator_id)
        teachers_root.mainloop()

    def open_subjects(self):
        self.root.destroy()
        subjects_root = tk.Tk()
        subjects_app = ManageSubjectsApp(subjects_root, self.coordinator_id)
        subjects_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenManager(root, coordinator_id=1)
    root.mainloop()