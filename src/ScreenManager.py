import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import os
from Pages.manageDisciplines import ManageSubjectsApp
from Pages.saved_grades import SavedGradesApp
from Pages.manageTeachers import ManageProfessorsApp
from Pages.userProfileApp import UserProfileApp

DB_NAME = "schedule.db"

class ScreenManager:
    def __init__(self, root, coordinator_id):
        self.root = root
        self.coordinator_id = coordinator_id
        self.icons_path = "C:/Users/sanvi/OneDrive/Documentos/GitHub/teacher-schedule/icons"

        self.root.title("GradeMaster")
        self.root.state('zoomed')  # Janela maximizada
        self.root.configure(bg="#F4F6FA")

        self.create_top_menu()
        self.create_main_content()

    def get_db_stats(self):
        """Busca estatísticas do banco de dados"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM disciplines WHERE coordinator_id=?", (self.coordinator_id,))
        courses_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM teachers WHERE coordinator_id=?", (self.coordinator_id,))
        teachers_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM saved_grades WHERE coordinator_id=?", (self.coordinator_id,))
        schedules_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "courses": courses_count,
            "teachers": teachers_count,
            "schedules": schedules_count
        }

    def create_top_menu(self):
        """Cria o menu superior sem fundo azul"""
        self.top_menu = tk.Frame(self.root, bg="#FFFFFF", height=70, 
                               highlightbackground="#E0E0E0", highlightthickness=1)
        self.top_menu.pack(side=tk.TOP, fill=tk.X)

        # Logo
        logo_frame = tk.Frame(self.top_menu, bg="#FFFFFF")
        logo_frame.pack(side=tk.LEFT, padx=20)

        try:
            logo_img = Image.open(os.path.join(self.icons_path, "frameCentral.png"))
            logo_img = logo_img.resize((40, 40), Image.Resampling.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(logo_frame, image=self.logo_image, bg="#FFFFFF")
            logo_label.pack(side=tk.LEFT, padx=(0, 10))
        except Exception as e:
            print(f"Erro ao carregar logo: {e}")
            logo_label = tk.Label(logo_frame, text="GM", font=("Helvetica", 20, "bold"), bg="#FFFFFF", fg="#2A72C3")
            logo_label.pack(side=tk.LEFT, padx=20)

        title_label = tk.Label(logo_frame, text="GradeMaster", font=("Helvetica", 16, "bold"), bg="#FFFFFF", fg="#2A72C3")
        title_label.pack(side=tk.LEFT)

        # Menu items
        menu_items = [
            ("Criar Grade", self.open_timetable),
            ("Grades Salvas", self.open_saved),
            ("Professores", self.open_teachers),
            ("Perfil", self.open_user_profile)
        ]

        menu_frame = tk.Frame(self.top_menu, bg="#FFFFFF")
        menu_frame.pack(side=tk.RIGHT, padx=20)

        for text, command in menu_items:
            btn = tk.Button(menu_frame, text=text, font=("Helvetica", 12), 
                           bg="#FFFFFF", fg="#555555", bd=0,
                           activebackground="#EEF1F8", activeforeground="#2A72C3",
                           cursor="hand2", command=command)
            btn.pack(side=tk.LEFT, padx=15)

    def create_main_content(self):
        self.main_content = tk.Frame(self.root, bg="#F4F6FA")
        self.main_content.pack(expand=True, fill=tk.BOTH)

        # Container central
        center_container = tk.Frame(self.main_content, bg="#F4F6FA")
        center_container.place(relx=0.5, rely=0.4, anchor="center")

        # Imagem central
        try:
            original_img = Image.open(os.path.join(self.icons_path, "frameCentral.png"))
            # Redimensiona mantendo proporção para altura máxima de 400px
            width, height = original_img.size
            new_height = 400
            new_width = int((new_height / height) * width)
            
            central_img = original_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.central_image = ImageTk.PhotoImage(central_img)
            
            img_label = tk.Label(center_container, image=self.central_image, bg="#F4F6FA")
            img_label.pack(pady=(0, 20))
        except Exception as e:
            print(f"Erro ao carregar imagem central: {e}")
            img_label = tk.Label(center_container, text="[Imagem ilustrativa]", 
                               font=("Helvetica", 16), bg="#F4F6FA", fg="#999999")
            img_label.pack(pady=(0, 20))

        # Botão Criar Grade
        create_btn = tk.Button(center_container, text="Criar Grade", 
                             font=("Helvetica", 14, "bold"), 
                             bg="#2A72C3", fg="white",
                             bd=0, padx=40, pady=10,
                             activebackground="#3A82D3", activeforeground="white",
                             cursor="hand2", command=self.open_timetable)
        create_btn.pack(pady=(0, 40))  # Espaço reduzido abaixo do botão

        # Stats cards
        stats_frame = tk.Frame(self.main_content, bg="#F4F6FA")
        stats_frame.place(relx=0.5, rely=0.8, anchor="center")

        stats = self.get_db_stats()
        
        self.create_stat_card(stats_frame, "Cursos", stats["courses"], "cursos.png")
        self.create_stat_card(stats_frame, "Professores", stats["teachers"], "professor.png")
        self.create_stat_card(stats_frame, "Horários", stats["schedules"], "frameCentral.png")

    def create_stat_card(self, parent, title, value, icon_name):
        card = tk.Frame(parent, bg="white", padx=25, pady=20, 
                        highlightbackground="#E0E0E0", highlightthickness=1)
        card.pack(side=tk.LEFT, padx=15)

        # Icon
        try:
            icon_path = os.path.join(self.icons_path, icon_name)
            icon_img = Image.open(icon_path)
            icon_img = icon_img.resize((40, 40), Image.Resampling.LANCZOS)
            self.icon_image = ImageTk.PhotoImage(icon_img)
            icon_label = tk.Label(card, image=self.icon_image, bg="white")
            icon_label.image = self.icon_image
            icon_label.pack(side=tk.LEFT, padx=(0, 15))
        except Exception as e:
            print(f"Erro ao carregar ícone {icon_name}: {e}")
            icon_label = tk.Label(card, text="[Ícone]", font=("Helvetica", 10), bg="white")
            icon_label.pack(side=tk.LEFT, padx=(0, 15))

        # Text content
        text_frame = tk.Frame(card, bg="white")
        text_frame.pack(side=tk.LEFT)

        title_label = tk.Label(text_frame, text=title, font=("Helvetica", 12, "bold"), 
                              bg="white", fg="#555555", anchor="w")
        title_label.pack()

        value_text = f"{value} {'cursos' if title == 'Cursos' else 'professores' if title == 'Professores' else 'grades'} {'cadastrados' if title != 'Horários' else 'geradas'}"
        value_label = tk.Label(text_frame, text=value_text, 
                              font=("Helvetica", 14), bg="white", fg="#2A72C3", anchor="w")
        value_label.pack(pady=(5, 0))

    # Funções de navegação (mantidas iguais)
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