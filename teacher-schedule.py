import tkinter as tk
from tkinter import ttk
import random

classes = [f"CC{i}" for i in range(1, 9)]
days_of_week = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
time_slots = [
    "19:10 - 20:25",  # 1ª aula
    "20:25 - 20:45",  # Intervalo
    "20:45 - 22:00"   # 2ª aula
]

teachers = {
    "Lidiana": ["Segunda", "Terça", "Sexta"],
    "Diogo": ["Segunda"],
    "Flávio": ["Terça", "Quarta"],
    "André": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"],
    "Jucilene": ["Quarta"],
    "Joao Otávio": ["Segunda", "Terça", "Quarta", "Quinta"],
    "Allan": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"],  # Apenas 3 dias
    "Valter": ["Terça", "Quarta"],
    "Fábio": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"],
    "Cícero": ["Segunda", "Terça", "Quarta"],
    "Elio": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"],  # Apenas 1 dia
    "Evandro": ["Quinta"],
    "Taisa": ["Segunda", "Quarta", "Quinta"],
    "Rogerio": ["Segunda", "Terça", "Quarta", "Quinta"],
    "Franco": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"],
    "Joao Marcelo": ["Segunda", "Terça", "Sexta"],
    "Janayna": ["Segunda"]
}

teacher_limits = {"Allan": 3, "Elio": 1}
teacher_allocations = {teacher: set() for teacher in teachers}

def generate_timetable():
    timetable = {cls: {day: {time_slot: None for time_slot in time_slots} for day in days_of_week} for cls in classes}
    
    for cls in classes:
        for day in days_of_week:
            previous_teacher = None
            for i, time_slot in enumerate(time_slots):
                available_teachers = [teacher for teacher, availability in teachers.items() 
                                      if day in availability 
                                      and (teacher not in teacher_limits or len(teacher_allocations[teacher]) < teacher_limits[teacher])]
                
                if time_slot == "20:25 - 20:45":  # Intervalo
                    teacher = "INTERVALO"
                elif not available_teachers:
                    teacher = "[SEM PROFESSOR]"
                else:
                    if previous_teacher and previous_teacher in available_teachers and random.random() < 0.2:
                        teacher = previous_teacher  
                    else:
                        teacher = random.choice([t for t in available_teachers if t != previous_teacher] or available_teachers)
                        teacher_allocations[teacher].add(day)
                
                timetable[cls][day][time_slot] = teacher
                previous_teacher = teacher
    return timetable

def display_timetable_gui(timetables):
    root = tk.Tk()
    root.title("Solução 1")

    canvas = tk.Canvas(root)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    timetable_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=timetable_frame, anchor="nw")

    def create_class_table(class_name, timetable_class):
        frame = tk.Frame(timetable_frame)
        frame.pack(padx=10, pady=10, anchor="w")
        
        label = tk.Label(frame, text=f"Grade para {class_name}", font=("Arial", 14))
        label.grid(row=0, column=0, columnspan=len(days_of_week) + 1)

        for i, day in enumerate(days_of_week):
            label = tk.Label(frame, text=day, font=("Arial", 12))
            label.grid(row=1, column=i+1, padx=5, pady=5)
        
        for row, time_slot in enumerate(time_slots, start=2):
            label = tk.Label(frame, text=time_slot, font=("Arial", 12))
            label.grid(row=row, column=0, padx=5, pady=5)
            for col, day in enumerate(days_of_week, start=1):
                teacher = timetable_class[day].get(time_slot, None)
                teacher_label = tk.Label(frame, text=teacher, font=("Arial", 10))
                teacher_label.grid(row=row, column=col, padx=5, pady=5)

    def update_timetable(timetable, solution_number):
        for widget in timetable_frame.winfo_children():
            widget.destroy()

        root.title(f"Solução {solution_number}")
        
        for class_name, timetable_class in timetable.items():
            create_class_table(class_name, timetable_class)

        timetable_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    solution_number = 0
    total_solutions = 5
    timetables = [generate_timetable() for _ in range(total_solutions)]
    
    def show_next_solution():
        nonlocal solution_number
        solution_number = (solution_number + 1) % total_solutions
        update_timetable(timetables[solution_number], solution_number + 1)

    next_button = tk.Button(root, text="Próxima Solução", command=show_next_solution)
    next_button.pack(pady=10)

    update_timetable(timetables[solution_number], solution_number + 1)

    root.mainloop()

if __name__ == "__main__":
    display_timetable_gui(None)
