import tkinter as tk
from tkinter import ttk
import random
import sqlite3
from style import style_tkinter_widgets  

def get_teachers_from_db():
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM teachers")
    teachers = {row[0]: [] for row in cursor.fetchall()}

    cursor.execute("SELECT teacher_id, day FROM teacher_availability")
    for teacher_id, day in cursor.fetchall():
        teacher_name = get_teacher_name_by_id(teacher_id, conn)
        if teacher_name in teachers:
            teachers[teacher_name].append(day)

    conn.close()
    return teachers

def get_teacher_name_by_id(teacher_id, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM teachers WHERE id = ?", (teacher_id,))
    result = cursor.fetchone()
    return result[0] if result else None

teachers = get_teachers_from_db()
teacher_limits = {"Allan": 3, "Elio": 1}
teacher_allocations = {teacher: set() for teacher in teachers}

classes = [f"CC{i}" for i in range(1, 9)] + [f"ADS{i}" for i in range(1, 5)]
days_of_week = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
time_slots = ["19:10 - 20:25", "20:25 - 20:45", "20:45 - 22:00"]

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
    root.title("Grade de Aulas")
    root.config(bg="#F4F6F9")
    style_frame, style_label = style_tkinter_widgets(root)  

    def create_class_table(class_name, timetable_class):
        frame = tk.Frame(timetable_frame, bg="#ffffff", relief="flat", borderwidth=0)
        style_frame(frame)
        frame.pack(padx=20, pady=20, fill="x", expand=True)

        label = tk.Label(frame, text=f"Grade para {class_name}", font=("Arial", 18, "bold"), bg="#00796B", fg="white")
        style_label(label, font_size=18, font_weight="bold", bg_color="#00796B", fg_color="white")  
        label.grid(row=0, column=0, columnspan=len(days_of_week) + 1, pady=10)

        for i, day in enumerate(days_of_week):
            label = tk.Label(frame, text=day, font=("Arial", 12, "bold"), bg="#00796B", fg="white")
            style_label(label, font_size=12, font_weight="bold", bg_color="#00796B", fg_color="white")  
            label.grid(row=1, column=i+1, padx=10, pady=10)

        for row, time_slot in enumerate(time_slots, start=2):
            label = tk.Label(frame, text=time_slot, font=("Arial", 12), bg="#B2DFDB", fg="black")
            style_label(label, font_size=12, bg_color="#B2DFDB", fg_color="black")  
            label.grid(row=row, column=0, padx=15, pady=5)
            for col, day in enumerate(days_of_week, start=1):
                teacher = timetable_class[day].get(time_slot, None)
                teacher_label = tk.Label(frame, text=teacher, font=("Arial", 10), bg="#FFFFFF", fg="black")
                style_label(teacher_label, font_size=10, bg_color="#FFFFFF", fg_color="black")  
                teacher_label.grid(row=row, column=col, padx=10, pady=5)

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

    canvas = tk.Canvas(root, bg="#F4F6F9", bd=0)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    timetable_frame = tk.Frame(canvas, bg="#F4F6F9")
    canvas.create_window((0, 0), window=timetable_frame, anchor="nw")

    next_button = tk.Button(root, text="Próxima Solução", command=show_next_solution, font=("Arial", 14), relief="raised", bg="#00796B", fg="white", padx=15, pady=10)
    style_label(next_button, font_size=14, bg_color="#00796B", fg_color="white") 
    next_button.pack(pady=20)

    update_timetable(timetables[0], 1)
    root.mainloop()

display_timetable_gui(generate_timetable())
