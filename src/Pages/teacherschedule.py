from os import name
import sqlite3
import tkinter as tk
from tkinter import ttk
import random
from tkinter import PhotoImage
from tkinter import filedialog
from tkinter import messagebox
from tkinter.messagebox import askyesno
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))  
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'DbContext'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'UserControl'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'CSS'))
from DbContext.database import DB_NAME
from DbContext.models import get_teachers
from CSS.style import *
from UserControl.config import get_class_course, get_disciplines, teachers, teacher_limits, classes, days_of_week, time_slots
from ScreenManager import ScreenManager
from UserControl.sidebar import create_sidebar
#from UserControl.button_design import create_action_buttons

class TimetableApp:
    def __init__(self, root):
        self.root = root
        self.teachers = self.get_teachers()
        self.root.title("Gerenciamento de Grade de Aulas")
        self.root.geometry("900x800")
        self.root.config(bg=BACKGROUND_COLOR)
        self.selected_cell = None
        self.teacher_allocations = {teacher: set() for teacher in teachers}
        self.selected_grades = []

        self.main_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        self.main_frame.pack(fill="both", expand=True)

        self.setup_ui()

    def setup_ui(self):
        self.sidebar_frame = create_sidebar(
            self.main_frame, 
            show_home_screen=self.show_home_screen,
            show_modules_screen=self.show_modules_screen,
            save_changes=self.save_changes
        )
        self.action_frame = tk.Frame(self.main_frame, bg=BACKGROUND_COLOR)
        self.action_frame.pack(pady=10, padx=10, fill="x")
       # create_action_buttons(self.action_frame, {
       #     "create": self.create_manual_schedule,
       #     "show_timetable": self.show_timetable,
       #     "edit_teacher": self.edit_teacher,
       #     "save_changes": self.save_changes,
       #     "cancel_edit": self.cancel_edit,
       #     "confirm_delete_schedule": self.confirm_delete_schedule,
       #     "download_grade": self.download_grade
       # })

        # Cabeçalho com o título
        self.header_frame = tk.Frame(self.main_frame, bg="#F8F8F8")
        self.header_frame.pack(pady=20, fill="x", padx=10)

        title_label = tk.Label(
            self.header_frame,
            text="Criar Grade",
            font=("Arial", 16, "bold"),
            bg="#F8F8F8",
            fg="#2A72C3",
            cursor="hand2",
            anchor="w"
        )
        title_label.pack(fill="x", padx=10)

        # Frame para os botões de ação
        self.action_frame = tk.Frame(self.main_frame, bg=BACKGROUND_COLOR)
        self.action_frame.pack(pady=10, padx=10, fill="x")

        # Carregamento dos ícones dos botões
        self.save_icon = PhotoImage(file="icons/salvar.png").subsample(20, 20)
        self.cancel_icon = PhotoImage(file="icons/cancel.png").subsample(20, 20)
        self.list_icon = PhotoImage(file="icons/list.png").subsample(20, 20)
        self.edit_icon = PhotoImage(file="icons/edit.png").subsample(20, 20)
        self.delete_icon = PhotoImage(file="icons/delete.png").subsample(20, 20)
        self.create_icon = PhotoImage(file="icons/mais.png").subsample(20, 20)
        self.download_icon = PhotoImage(file="icons/download.png").subsample(20, 20)

        # Botões de ação dentro do frame action_frame
        self.create_button = tk.Button(
            self.action_frame,
            image=self.create_icon,
            command=self.create_manual_schedule,
            padx=8,
            pady=4,
            borderwidth=0,
            relief="flat",
            highlightthickness=0,
            activebackground=BACKGROUND_COLOR
        )
        self.create_button.pack(side="left", padx=8)

        self.list_button = tk.Button(
            self.action_frame,
            image=self.list_icon,
            command=self.show_timetable,
            padx=8,
            pady=4,
            borderwidth=0,
            relief="flat",
            highlightthickness=0,
            activebackground=BACKGROUND_COLOR
        )
        self.list_button.pack(side="left", padx=8)

        self.edit_button = tk.Button(
            self.action_frame,
            image=self.edit_icon,
            command=self.edit_cell,
            state="disabled",
            padx=8,
            pady=4,
            borderwidth=0,
            relief="flat",
            highlightthickness=0,
            activebackground=BACKGROUND_COLOR
        )
        self.edit_button.pack(side="left", padx=8)

        self.save_button = tk.Button(
            self.action_frame,
            image=self.save_icon,
            command=self.save_changes,
            state="disabled",
            padx=8,
            pady=4,
            borderwidth=0,
            relief="flat",
            highlightthickness=0,
            activebackground=BACKGROUND_COLOR
        )
        self.save_button.pack(side="left", padx=8)

        self.cancel_button = tk.Button(
            self.action_frame,
            image=self.cancel_icon,
            command=self.cancel_edit,
            state="disabled",
            padx=8,
            pady=4,
            borderwidth=0,
            relief="flat",
            highlightthickness=0,
            activebackground=BACKGROUND_COLOR
        )
        self.cancel_button.pack(side="left", padx=8)

        self.delete_button = tk.Button(
            self.action_frame,
            image=self.delete_icon,
            command=self.confirm_delete_schedule,
            state="disabled",
            padx=8,
            pady=4,
            borderwidth=0,
            relief="flat",
            highlightthickness=0,
        )
        self.delete_button.pack(side="left", padx=8)

        self.download_button = tk.Button(
            self.action_frame,
            image=self.download_icon,
            command=self.download_grade,
            state="disabled",
            padx=8,
            pady=4,
            borderwidth=0,
            relief="flat",
            highlightthickness=0,
        )
        self.download_button.pack(side="left", padx=8)

        # Área para exibição da grade de aulas
        self.timetable_frame = tk.Frame(self.main_frame, bg=BACKGROUND_COLOR)
        self.timetable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.scroll_canvas = tk.Canvas(self.timetable_frame)
        self.scroll_frame = tk.Frame(self.scroll_canvas, bg=BACKGROUND_COLOR)
        self.scroll_bar = tk.Scrollbar(self.timetable_frame, orient="vertical", command=self.scroll_canvas.yview)
        self.scroll_canvas.configure(yscrollcommand=self.scroll_bar.set)

        self.scroll_bar.pack(side="right", fill="y")
        self.scroll_canvas.pack(side="left", fill="both", expand=True)
        self.scroll_canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
        )
        
    def get_teachers(self):
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, max_days FROM teachers")
        teachers = cursor.fetchall()
        conn.close()
        return teachers
    
    def show_modules_screen(self):
        """Expande ou recolhe o painel de módulos."""
        if self.modules_frame.winfo_ismapped():
            self.modules_frame.pack_forget()  
        else:
            self.modules_frame.pack(pady=10, padx=10, fill="x")  

    def show_home_screen(self):
        """Retorna à tela inicial."""
        self.root.destroy()
        home_root = tk.Tk()
        app = ScreenManager(home_root)
        home_root.mainloop()

    def generate_timetable(self):
        disciplines = get_disciplines()
        teachers = get_teachers()
        
        timetable = {cls: {day: {time_slot: {'discipline': '', 'teacher': ''} for time_slot in time_slots} for day in days_of_week} for cls in classes}

        for cls in classes:
            class_course = get_class_course(cls)
            class_disciplines = [d for d in disciplines if d['course'] == class_course]

            discipline_hours = {d['name']: d['hours'] for d in class_disciplines}
            assigned_hours = {d['name']: 0 for d in class_disciplines}

            for day in days_of_week:
                previous_teacher = None
                for time_slot in time_slots:
                    available_teachers = list(teachers)
                    
                    if time_slot == "20:25 - 20:45":  # Intervalo
                        teacher = "INTERVALO"
                        discipline = ""
                    else:
                        possible_disciplines = [d for d in class_disciplines if assigned_hours[d['name']] < discipline_hours[d['name']]]
                        
                        if possible_disciplines:
                            discipline_obj = random.choice(possible_disciplines)
                            discipline = discipline_obj['name']
                            assigned_hours[discipline] += 1
                        else:
                            discipline = None
                        
                        if available_teachers and discipline:
                            teacher_tuple = random.choice(available_teachers)
                            teacher = teacher_tuple[1]
                        else:
                            teacher = ""

                        if teacher not in self.teacher_allocations:
                            self.teacher_allocations[teacher] = set()
                        self.teacher_allocations[teacher].add(day)
                    
                    timetable[cls][day][time_slot] = {'discipline': discipline, 'teacher': teacher}
                    previous_teacher = teacher

            # Verificação da carga horária distribuída
            print("\n🔍 Verificação das Horas Alocadas por Disciplina 🔍")
            for cls in timetable:
                discipline_count = {}

                for day in timetable[cls]:
                    for time_slot, details in timetable[cls][day].items():
                        discipline = details['discipline']
                        if discipline and discipline != "INTERVALO":
                            if discipline not in discipline_count:
                                discipline_count[discipline] = 0
                            discipline_count[discipline] += 1

                print(f"\n📌 Turma: {cls}")
                for discipline, allocated_hours in discipline_count.items():
                    expected_hours = next(d['hours'] for d in disciplines if d['name'] == discipline)
                    print(f"  - {discipline}: {allocated_hours} aulas (Esperado: {expected_hours})")

        return timetable

    def show_timetable(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        self.timetable = self.generate_timetable()
        
        for name, timetable_class in self.timetable.items():
            self.create_class_table(self.scroll_frame, name, timetable_class)
    
    def create_class_table(self, parent, name, timetable_class):
        frame = tk.Frame(parent, bg=WHITE_COLOR, relief="solid", borderwidth=1)
        frame.pack(padx=20, pady=10, fill="x", expand=True)

        header = tk.Frame(frame)
        header.grid(row=0, column=0, columnspan=len(days_of_week) + 2, sticky="ew")
        
        header_label = tk.Label(header, text=f"Grade para {name}", font=HEADER_FONT, fg=TEXT_COLOR)
        header_label.pack(side="left", padx=10, pady=5)
        
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(header, variable=var, command=lambda: self.select_grade(name, var))
        checkbox.pack(side="right", padx=10, pady=5)
        
        # Primeira linha de cabeçalhos para os dias da semana
        tk.Label(frame, text="", font=LABEL_FONT, fg=TEXT_COLOR, relief="ridge", borderwidth=1).grid(row=1, column=0, padx=6, pady=6, sticky="nsew")
        for i, day in enumerate(days_of_week):
            day_label = tk.Label(frame, text=day, font=LABEL_FONT, fg=TEXT_COLOR, relief="ridge", borderwidth=1)
            day_label.grid(row=1, column=i+1, padx=6, pady=6, sticky="nsew")
        
        for row, time_slot in enumerate(time_slots, start=2):
            time_label = tk.Label(frame, text=time_slot, font=TIME_SLOT_FONT, bg=LABEL_COLOR, fg=TEXT_COLOR, relief="ridge", borderwidth=1)
            time_label.grid(row=row, column=0, padx=10, pady=3, sticky="nsew")
            
            # Acessando as disciplinas e professores para cada horário
            for col, day in enumerate(days_of_week, start=1):
                discipline_info = timetable_class.get(day, {}).get(time_slots[row - 2], {'[SEM DISCIPLINA]', '[SEM PROFESSOR]'})
                discipline = discipline_info['discipline']
                teacher = discipline_info['teacher']
                
                # Exibindo o nome do professor e a disciplina na célula
                cell_label = tk.Label(frame, text=f"{discipline}\n{teacher}", font=TEACHER_FONT, bg=WHITE_COLOR, fg=TEXT_COLOR,
                                    padx=8, pady=4, relief="groove", borderwidth=1)
                cell_label.grid(row=row, column=col, padx=6, pady=3, sticky="nsew")
                cell_label.bind("<Button-1>", lambda e, d=day, t=time_slot, l=cell_label: self.select_cell(d, t, l))

    def select_grade(self, grade_name, var):
        if var.get():
            if grade_name not in self.selected_grades:
                self.selected_grades.append(grade_name)
        else:
            if grade_name in self.selected_grades:
                self.selected_grades.remove(grade_name)

        if self.selected_grades:
            self.download_button.config(state="normal")
        else:
            self.download_button.config(state="disabled")
            
    DB_NAME = "schedule.db"

    def download_grade(self):
        if not self.selected_grades:
            messagebox.showwarning("Aviso", "Nenhuma grade selecionada para download.")
            return

        for grade_name in self.selected_grades:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt", 
                filetypes=[("Text files", "*.txt")],
                initialfile=f"{grade_name}.txt"
            )

            if not file_path:
                continue  

            timetable_class = self.timetable.get(grade_name, {})

            print(f"📌 Baixando grade: {grade_name}")
            print(timetable_class)

            grade_content = f"Grade de {grade_name}\n"

            for day in days_of_week:
                grade_content += f"\n{day}:\n"
                schedule = timetable_class.get(day, {})

                if isinstance(schedule, dict):
                    for time_slot, teacher in schedule.items():
                        grade_content += f"{time_slot}: {teacher}\n"
                elif isinstance(schedule, list):
                    for entry in schedule:
                        grade_content += f"{entry}\n"

            grade_content += "\n" + "=" * 30 + "\n"

            print("📌 Dados salvos no arquivo:\n", grade_content)  

            with open(file_path, "w") as f:
                f.write(grade_content)

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO saved_grades (name, content, file_path)
                VALUES (?, ?, ?)
            """, (grade_name, grade_content, file_path))

            conn.commit()
            conn.close()

        messagebox.showinfo("Sucesso", "Grade(s) baixada(s) com sucesso e salvas no banco!")

    def select_cell(self, day, time_slot, label):
        if self.selected_cell:
            self.selected_cell.config(bg=WHITE_COLOR)
        
        self.selected_cell = label
        self.selected_cell.config(bg=LABEL_COLOR)
        
        text = self.selected_cell.cget("text")
        self.original_discipline = text.split("\n")[0]  
        self.original_teacher = text.split("\n")[1]   
        
        self.edit_button.config(state="normal")
        self.save_button.config(state="normal")
        self.cancel_button.config(state="normal")
        self.delete_button.config(state="normal")


    def edit_cell(self):
        if not self.selected_cell:
            return
        
        self.original_teacher = self.selected_cell.cget("text").split("\n")[1]
        self.original_discipline = self.selected_cell.cget("text").split("\n")[0]
        self.open_edit_modal()

    def open_edit_modal(self):
        modal_window = tk.Toplevel(self.root)
        modal_window.title("Editar Disciplina e Professor")
        
        label_discipline = tk.Label(modal_window, text="Selecione uma nova disciplina:")
        label_discipline.pack(pady=4)
        
        discipline_select = ttk.Combobox(modal_window, values=[d['name'] for d in get_disciplines()])
        discipline_select.set(self.original_discipline)
        discipline_select.pack(pady=4)
        
        label_teacher = tk.Label(modal_window, text="Selecione um novo professor:")
        label_teacher.pack(pady=4)
        
        teacher_select = ttk.Combobox(modal_window, values=list(teachers.keys()))
        teacher_select.set(self.original_teacher)
        teacher_select.pack(pady=4)
        
        def save_changes():
            new_discipline = discipline_select.get()
            new_teacher = teacher_select.get()
            self.selected_cell.config(text=f"{new_discipline}\n{new_teacher}")
            
            self.original_discipline = new_discipline
            self.original_teacher = new_teacher
            
            modal_window.destroy()
            self.save_button.config(state="disabled")
            self.cancel_button.config(state="disabled")

        def cancel():
            modal_window.destroy()

        save_button = tk.Button(modal_window, text="Salvar", command=save_changes)
        save_button.pack(pady=4)
        
        cancel_button = tk.Button(modal_window, text="Cancelar", command=cancel)
        cancel_button.pack(pady=4)

    def save_changes(self):
        if self.selected_cell:
            self.save_button.config(state="disabled")
            self.cancel_button.config(state="disabled")

    def cancel_edit(self):
        if self.selected_cell:
            self.selected_cell.config(text=f"{self.original_discipline}\n{self.original_teacher}")
        
        self.save_button.config(state="disabled")
        self.cancel_button.config(state="disabled")
        
    def confirm_delete_schedule(self):
        if self.selected_cell:
            confirmation = askyesno("Confirmar Exclusão", "Você tem certeza que deseja excluir este registro?")
            if confirmation:
                self.delete_schedule()
    
    def delete_schedule(self):
        if self.selected_cell:
            self.selected_cell.config(text="[REMOVIDO]")
            self.selected_cell.config(bg=WHITE_COLOR)
            self.selected_cell = None
            self.edit_button.config(state="disabled")
            self.delete_button.config(state="disabled")
            self.save_button.config(state="disabled")
            self.cancel_button.config(state="disabled")

    def create_manual_schedule(self):
        manual_schedule_window = tk.Toplevel(self.root)
        manual_schedule_window.title("Criar Grade Manualmente")
        
        class_label = tk.Label(manual_schedule_window, text="Escolha a Turma:")
        class_label.pack(pady=8)
        
        class_select = ttk.Combobox(manual_schedule_window, values=classes)
        class_select.pack(pady=8)
        
        def save_manual_schedule():
            selected_class = class_select.get()
           
            self.timetable[selected_class]= selected_class
            manual_schedule_window.destroy()
            self.show_timetable()
        
        save_button = tk.Button(manual_schedule_window, text="Salvar", command=save_manual_schedule)
        save_button.pack(pady=8)
    
if __name__ == "__main__":
    root = tk.Tk()
    app = TimetableApp(root)
    root.mainloop()
