import tkinter as tk
from tkinter import ttk
import random
import sqlite3
from style import *
from DbContext.models import get_teachers, update_teacher_availability, get_teacher_availability
from config import teachers, teacher_limits, classes, days_of_week, time_slots
from DbContext.database import DB_NAME

def get_teachers_from_db():
    return list(teachers.keys())

teachers = get_teachers_from_db()

teacher_allocations = {teacher: set() for teacher in teachers}

def generate_timetable():
    timetable = {cls: {day: {time_slot: None for time_slot in time_slots} for day in days_of_week} for cls in classes}

    for cls in classes:
        for day in days_of_week:
            previous_teacher = None
            for i, time_slot in enumerate(time_slots):
                available_teachers = [teacher for teacher in teachers
                                      if teacher not in teacher_limits or len(teacher_allocations[teacher]) < teacher_limits.get(teacher, float('inf'))]

                if time_slot == "20:25 - 20:45": 
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

def update_teacher_in_db(name, day, time_slot, new_teacher):
    conn = sqlite3.connect("schedule.db")
    teacher_id = None
    for teacher in get_teachers():  
        if teacher[1] == new_teacher:  
            teacher_id = teacher[0]
            break

    if teacher_id:
        update_teacher_availability(teacher_id, day, new_teacher)  

    conn.close()

def display_timetable_gui(timetables):
    root = tk.Tk()
    root.title("Grade de Aulas")
    root.config(bg=BACKGROUND_COLOR)
    
    canvas = tk.Canvas(root, bg=BACKGROUND_COLOR)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.config(yscrollcommand=scrollbar.set)

    timetable_frame = tk.Frame(canvas, bg=BACKGROUND_COLOR)
    canvas.create_window((0, 0), window=timetable_frame, anchor="nw")

    def create_class_table(name, timetable_class):
        frame = tk.Frame(timetable_frame, bg=WHITE_COLOR, relief="flat", borderwidth=0)
        frame.pack(padx=20, pady=20, fill="x", expand=True)

        label = tk.Label(frame, text=f"Grade para {name}", font=HEADER_FONT, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
        label.grid(row=0, column=0, columnspan=len(days_of_week) + 1, pady=10)

        for i, day in enumerate(days_of_week):
            label = tk.Label(frame, text=day, font=LABEL_FONT, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
            label.grid(row=1, column=i+1, padx=10, pady=10)

        for row, time_slot in enumerate(time_slots, start=2):
            label = tk.Label(frame, text=time_slot, font=TIME_SLOT_FONT, bg=LABEL_COLOR, fg=TEXT_COLOR)
            label.grid(row=row, column=0, padx=15, pady=5)

            for col, day in enumerate(days_of_week, start=1):
                teacher = timetable_class[day].get(time_slot, None)
                teacher_label = tk.Label(frame, text=teacher, font=TEACHER_FONT, bg=WHITE_COLOR, fg=TEXT_COLOR)
                teacher_label.grid(row=row, column=col, padx=10, pady=5)

                edit_button = tk.Button(frame, text="Editar", command=lambda cls=name, d=day, ts=time_slot, teacher=teacher, label=teacher_label: edit_teacher(cls, d, ts, teacher, label))
                edit_button.grid(row=row, column=col+1, padx=5)

    def edit_teacher(name, day, time_slot, teacher, teacher_label):
        edit_window = tk.Toplevel(root)
        edit_window.title(f"Editar Professor - {name} - {day} - {time_slot}")

        label = tk.Label(edit_window, text="Selecione um novo professor:")
        label.pack(pady=10)

        teacher_select = ttk.Combobox(edit_window, values=teachers)
        teacher_select.set(teacher)  
        teacher_select.pack(pady=10)

        def save_changes():
            new_teacher = teacher_select.get()
            if new_teacher and new_teacher != teacher:

                update_teacher_in_db(name, day, time_slot, new_teacher)
                edit_window.destroy()

                teacher_label.config(text=new_teacher)

        save_button = tk.Button(edit_window, text="Salvar", command=save_changes)
        save_button.pack(pady=20)

    def generate_and_update_timetable():
        timetables = generate_timetable()
        update_timetable(timetables)  

    def update_timetable(timetable):
        for widget in timetable_frame.winfo_children():
            widget.destroy()

        for name, timetable_class in timetable.items():
            create_class_table(name, timetable_class)

        timetable_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    timetables = [generate_timetable() for _ in range(5)]
    solution_number = 0

    def show_next_solution():
        nonlocal solution_number
        solution_number = (solution_number + 1) % 5
        update_timetable(timetables[solution_number])

    next_button = tk.Button(root, text="Próxima Solução", command=show_next_solution)
    next_button.pack(pady=20)

    update_timetable(timetables[0])
    root.mainloop()

display_timetable_gui(generate_timetable())

