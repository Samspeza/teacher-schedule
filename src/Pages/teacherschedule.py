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
from UserControl.config import get_class_course, get_class_id, get_disciplines, get_teacher_availability_for_timetable, get_teacher_data, get_teacher_limits,  coordinator_id, teachers, teacher_limits, classes, days_of_week, time_slots
from ScreenManager import ScreenManager
from UserControl.sidebar import create_sidebar

class TimetableApp:
    def __init__(self, root, coordinator_id):
        self.root = root
        self.coordinator_id = coordinator_id
        self.teachers = self.get_teachers(self.coordinator_id)
        self.root.title("Gerenciamento de Grade de Aulas")
        self.root.geometry("900x800")
        self.root.config(bg=BACKGROUND_COLOR)
        self.selected_cell = None
        self.selected_grades = []

        self.teacher_allocations = {teacher: set() for teacher in self.teachers}

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

        self.lab_config_button = tk.Button(
            self.action_frame,
            text="Configurar Laboratórios",
            command=self.open_lab_config_window,
            padx=8,
            pady=4,
            bg="#DDEEFF",
            fg="#003366",
            font=("Arial", 10, "bold"),
            relief="raised"
        )
        self.lab_config_button.pack(side="left", padx=8)

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
        
    def get_teachers(self, coordinator_id):

        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, coordinator_id FROM teachers WHERE coordinator_id = ?", (coordinator_id,))
        
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
        app = ScreenManager(home_root, self.coordinator_id)
        home_root.mainloop()

    def get_coordinator_info(self):
        """Recupera informações do coordenador com base no ID"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT course FROM coordinators WHERE id = ?", (self.coordinator_id,))
        course = cursor.fetchone()
        conn.close()
        return course[0] if course else None
    
    def get_filtered_classes(self):
        """Retorna apenas as turmas associadas ao coordenador logado."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM classes WHERE coordinator_id = ?", (self.coordinator_id,))
        classes = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return classes

    def get_lab_disciplines_for_class(self, class_name):
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT d.name
            FROM disciplines d
            JOIN classes c ON d.course = c.name
            WHERE c.name = ? AND d.requires_laboratory = 1 AND d.coordinator_id = ?
        """, (class_name, self.coordinator_id))
        disciplines = [row[0] for row in cursor.fetchall()]
        conn.close()
        return disciplines

    def save_lab_division_config(self, class_name, discipline_name, division_count):
            conn = sqlite3.connect(self.DB_NAME)
            cursor = conn.cursor()
            
            # Buscar IDs correspondentes
            cursor.execute("SELECT id FROM classes WHERE name = ? AND coordinator_id = ?", (class_name, self.coordinator_id))
            class_id = cursor.fetchone()

            cursor.execute("SELECT id FROM disciplines WHERE name = ? AND coordinator_id = ?", (discipline_name, self.coordinator_id))
            discipline_id = cursor.fetchone()

            if class_id and discipline_id:
                cursor.execute("""
                    INSERT INTO lab_division_config (class_id, discipline_id, division_count, coordinator_id)
                    VALUES (?, ?, ?, ?)
                """, (class_id[0], discipline_id[0], division_count, self.coordinator_id))
                conn.commit()

            conn.close()
            
    def open_lab_config_window(self):
        window = tk.Toplevel(self.root)
        window.title("Configurar Laboratórios")
        window.geometry("400x300")
        
        tk.Label(window, text="Turma:").pack(pady=5)
        class_var = tk.StringVar()
        class_options = self.get_filtered_classes()
        class_dropdown = ttk.Combobox(window, textvariable=class_var, values=class_options, state="readonly")
        class_dropdown.pack()

        tk.Label(window, text="Disciplina com Laboratório:").pack(pady=5)
        discipline_var = tk.StringVar()
        discipline_dropdown = ttk.Combobox(window, textvariable=discipline_var, state="readonly")
        discipline_dropdown.pack()

        # Atualiza as disciplinas quando uma turma é selecionada
        def update_discipline_options(event):
            selected_class = class_var.get()
            disciplines = self.get_lab_disciplines_for_class(selected_class)
            discipline_dropdown['values'] = disciplines
            discipline_var.set("")  # Limpa a seleção anterior

        class_dropdown.bind("<<ComboboxSelected>>", update_discipline_options)

        tk.Label(window, text="Quantidade de Divisões:").pack(pady=5)
        division_entry = tk.Entry(window)
        division_entry.pack()

        def save_config():
            class_name = class_var.get()
            discipline_name = discipline_var.get()
            division_count = division_entry.get()

            if not class_name or not discipline_name or not division_count.isdigit():
                messagebox.showwarning("Atenção", "Preencha todos os campos corretamente.")
                return

            self.save_lab_division_config(class_name, discipline_name, int(division_count))
            messagebox.showinfo("Sucesso", "Configuração salva com sucesso!")
            window.destroy()

        save_btn = tk.Button(window, text="Salvar", command=save_config, bg="#B4E197")
        save_btn.pack(pady=20)


    def generate_timetable(self):
        """Gera o horário apenas para turmas do curso do coordenador, levando em conta disciplinas de laboratório."""
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        disciplines = get_disciplines(self.coordinator_id)
        teachers = get_teacher_data(self.coordinator_id)  
        teacher_limits = get_teacher_limits(self.coordinator_id)
        
        classes = self.get_filtered_classes()
        if not classes:
            print("⚠️ Nenhuma turma encontrada para este coordenador.")
            return {}

        timetable = {cls: {day: [['', ''] for _ in time_slots] for day in days_of_week} for cls in classes}
        availability_per_teacher = get_teacher_availability_for_timetable(teacher_limits, teachers)

        for cls in classes:
            class_course = get_class_course(cls, self.coordinator_id)  
            class_disciplines = [d for d in disciplines if d['course'] == class_course]  

            discipline_hours = {d['name']: d['hours'] for d in class_disciplines}  
            assigned_hours = {d['name']: 0 for d in class_disciplines}  

            # Buscar configurações de divisão de laboratório para a turma
            cursor.execute("""
                SELECT discipline_id, division_count 
                FROM lab_division_config 
                WHERE class_id = ? AND coordinator_id = ?
            """, (get_class_id(cls, self.coordinator_id), self.coordinator_id))
            lab_division_map = {row[0]: row[1] for row in cursor.fetchall()}

            # Organizar disciplinas por ID para buscar nome e requires_laboratory
            discipline_map = {d['id']: d for d in class_disciplines}

            for day in days_of_week:
                for i, time_slot in enumerate(time_slots):
                    if time_slot == "20:25 - 20:45":
                        timetable[cls][day][i] = ["", "INTERVALO"]
                        continue

                    available_teachers_for_day = [t for t in teachers if day in availability_per_teacher.get(t, [])]

                    # Obter disciplinas ainda não totalmente alocadas
                    possible_disciplines = [
                        d for d in class_disciplines if assigned_hours[d['name']] < discipline_hours[d['name']]
                    ]
                    if not possible_disciplines:
                        timetable[cls][day][i] = ["", ""]
                        continue

                    discipline_obj = random.choice(possible_disciplines)
                    discipline_name = discipline_obj['name']
                    discipline_id = discipline_obj['id']
                    requires_lab = discipline_obj.get('requires_laboratory', False)

                    if requires_lab and discipline_id in lab_division_map:
                        division_count = lab_division_map[discipline_id]
                        horas_por_divisao = int(discipline_hours[discipline_name] / division_count)
                        if assigned_hours[discipline_name] >= horas_por_divisao * division_count:
                            continue  # já alocado totalmente

                        divisao_atual = int(assigned_hours[discipline_name] / horas_por_divisao) + 1
                        disciplina_label = f"{discipline_name} (Lab {divisao_atual})"

                        # Evitar repetir o mesmo professor no mesmo dia (para simular divisão)
                        possible_teachers = [t for t in available_teachers_for_day if day not in self.teacher_allocations.get(t, set())]
                        teacher = random.choice(possible_teachers) if possible_teachers else ""
                    else:
                        disciplina_label = discipline_name
                        teacher = random.choice(available_teachers_for_day) if available_teachers_for_day else ""

                    assigned_hours[discipline_name] += 1
                    self.teacher_allocations.setdefault(teacher, set()).add(day)
                    timetable[cls][day][i] = [disciplina_label, teacher]

        conn.close()
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
        
        # Adicionando os horários
        for row, time_slot in enumerate(time_slots, start=2):
            time_label = tk.Label(frame, text=time_slot, font=TIME_SLOT_FONT, bg=LABEL_COLOR, fg=TEXT_COLOR, relief="ridge", borderwidth=1)
            time_label.grid(row=row, column=0, padx=10, pady=3, sticky="nsew")
            
            # Acessando as disciplinas e professores para cada horário
            for col, day in enumerate(days_of_week, start=1):
                cell_data = timetable_class[day][row - 2]
                discipline = cell_data[0]
                teacher = cell_data[1] if cell_data[1] else "[SEM PROFESSOR]"

                # Destacar visualmente laboratórios
                if "(Lab" in discipline:
                    cell_bg = "#E6F7FF"  # azul claro para laboratório
                elif "INTERVALO" in teacher:
                    cell_bg = "#F0F0F0"  # cinza claro para intervalo
                else:
                    cell_bg = WHITE_COLOR

                # Exibindo o nome do professor e a disciplina na célula
                cell_label = tk.Label(
                    frame, 
                    text=f"{discipline}\n{teacher}", 
                    font=TEACHER_FONT, 
                    bg=cell_bg, 
                    fg=TEXT_COLOR,
                    padx=8, pady=4, relief="groove", borderwidth=1
                )
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

            time_slots = ["19:10 - 20:25", "20:25 - 20:45", "20:45 - 22:00"]
            days_of_week = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]

            for day in days_of_week:
                grade_content += f"\n{day}:\n"
                schedule = timetable_class.get(day, [])

                if isinstance(schedule, list):
                    for i, entry in enumerate(schedule):
                        if i < len(time_slots): 
                            time_slot = time_slots[i]
                            discipline, teacher = entry                        
                           
                            if not discipline:
                                discipline = "-"
                            
                            grade_content += f"{time_slot}: {discipline} - {teacher}\n"                   
                    
                    if len(schedule) < len(time_slots):
                        for j in range(len(schedule), len(time_slots)):
                            grade_content += f"Horário desconhecido: {time_slots[j]}\n"
                
                    for slot in schedule:
                        if isinstance(slot, list) and len(slot) == 2:
                            discipline, teacher = slot
                            time_slot = "Horário desconhecido"  
                        else:
                            print("🚨 Formato inesperado de slot:", slot)
                            continue  

                        grade_content += f"{time_slot}: {discipline} - {teacher}\n"

            grade_content += "\n" + "=" * 30 + "\n"

            print("📌 Dados salvos no arquivo:\n", grade_content)  

            with open(file_path, "w") as f:
                f.write(grade_content)

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO saved_grades (name, content, file_path, coordinator_id)
            VALUES (?, ?, ?, ?)
            """, (grade_name, grade_content, file_path, self.coordinator_id))

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

        discipline_select = ttk.Combobox(modal_window, values=[d['name'] for d in get_disciplines(self.coordinator_id)])
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

            for cls, schedule in self.timetable.items():
                for day, slots in schedule.items():
                    for i, (discipline, teacher) in enumerate(slots):
                        if (discipline, teacher) == (self.original_discipline, self.original_teacher):
                            self.timetable[cls][day][i] = [new_discipline, new_teacher]

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
