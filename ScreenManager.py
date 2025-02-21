import tkinter as tk
from saved_grades import SavedGradesApp

class ScreenManager:
    def __init__(self, root): 
        self.root = root
        self.root.title("Módulo Menu")
        self.root.geometry("650x600")
        self.root.configure(bg="#F8F8F8")
        
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

    def open_timetable(self):
        """Abre a tela de criação de grade"""
        self.root.destroy()
        from teacherschedule import TimetableApp

        timetable_root = tk.Tk()
        app = TimetableApp(timetable_root)
        timetable_root.mainloop()

    def open_saved(self):
        """Abre a tela de grades salvas"""
        self.root.destroy()
        saved_root = tk.Tk()
        saved_app = SavedGradesApp(saved_root)
        saved_root.mainloop()

if __name__ == "__main__": 
    root = tk.Tk()
    app = ScreenManager(root)
    root.mainloop()