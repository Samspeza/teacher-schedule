import tkinter as tk
from tkinter import PhotoImage
from Pages.manageDisciplines import ManageSubjectsApp
from Pages.saved_grades import SavedGradesApp
from Pages.manageTeachers import ManageTeachersApp
from Pages.userProfileApp import UserProfileApp  
import sys
import os
from DbContext.database import DB_NAME
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'DbContext')))

class ScreenManager:
    def __init__(self, root, coordinator_id): 
        self.root = root
        self.coordinator_id = coordinator_id  
        
        self.root.title("Módulo Menu")
        self.root.geometry("900x800")
        self.root.configure(bg="#F8F8F8")
        
        # Frame do cabeçalho
        header_frame = tk.Frame(self.root, bg="#F8F8F8")
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.user_icon = tk.PhotoImage(file="icons/list.png").subsample(10, 10)  # Reduzindo pela metade
        self.user_button = tk.Button(
            header_frame, image=self.user_icon, command=self.open_user_profile, 
            bg="#F8F8F8", bd=0, cursor="hand2"
        )
        self.user_button.pack(side=tk.RIGHT)

        
        # Frame central
        central_frame = tk.Frame(self.root, bg="#F8F8F8")
        central_frame.pack(expand=True)

        self.icon_label = tk.Label(central_frame, text="🎓", font=("Arial", 60), bg="#F8F8F8", fg="#2A72C3")
        self.icon_label.pack(pady=20)
        
        self.menu_label = tk.Label(central_frame, text="TEACHER SCHEDULE", font=("Arial", 20, "bold"), bg="#F8F8F8", fg="#2A72C3")
        self.menu_label.pack(pady=20)
        
        # Botões
        self.create_button = tk.Button(central_frame, text="CRIAR GRADE", font=("Arial", 16), command=self.open_timetable, bg="#2A72C3", fg="white", width=15, height=2)
        self.create_button.pack(pady=20)
        
        self.saved_button = tk.Button(central_frame, text="SALVOS", font=("Arial", 16), command=self.open_saved, bg="#2A72C3", fg="white", width=15, height=2)
        self.saved_button.pack(pady=20)
        
        self.teachers_button = tk.Button(central_frame, text="CADASTROS", font=("Arial", 16), command=self.open_teachers, bg="#2A72C3", fg="white", width=15, height=2)
        self.teachers_button.pack(pady=20)

        self.subjects_button = tk.Button(central_frame, text="CADASTRAR DISCIPLINA", font=("Arial", 16), command=self.open_subjects, bg="#2A72C3", fg="white", width=20, height=2)
        self.subjects_button.pack(pady=20)
    
    def open_user_profile(self):
        """Abre a tela de edição de perfil do usuário."""
        self.root.destroy()
        user_root = tk.Tk()
        user_app = UserProfileApp(user_root, self.coordinator_id)
        user_root.mainloop()

    def open_timetable(self):
        """Abre a tela de criação de grade."""
        self.root.destroy()
        from Pages.teacherschedule import TimetableApp

        timetable_root = tk.Tk()
        app = TimetableApp(timetable_root, self.coordinator_id)  
        timetable_root.mainloop()

    def open_saved(self):
        """Abre a tela de grades salvas."""
        self.root.destroy()
        saved_root = tk.Tk()
        saved_app = SavedGradesApp(saved_root, self.coordinator_id)
        saved_root.mainloop()

    def open_teachers(self):
        """Abre a tela de gerenciamento de professores."""
        self.root.destroy()
        teachers_root = tk.Tk()
        teachers_app = ManageTeachersApp(teachers_root, self.coordinator_id)
        teachers_root.mainloop()

    def open_subjects(self):
        """Abre a tela de cadastro de disciplinas."""
        self.root.destroy()
        subjects_root = tk.Tk()
        subjects_app = ManageSubjectsApp(subjects_root, self.coordinator_id) 
        subjects_root.mainloop()

if __name__ == "__main__": 
    root = tk.Tk()
    app = ScreenManager(root)  
    root.mainloop()