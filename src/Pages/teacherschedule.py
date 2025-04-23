from os import name
import sqlite3
import tkinter as tk
from tkinter import ttk
import random
import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Alignment
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
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
from UserControl.config import get_available_lab, get_class_course, get_class_id, get_disciplines, get_laboratories, get_teacher_availability_for_timetable, get_teacher_data, get_teacher_limits,  coordinator_id, teachers, teacher_limits, classes, days_of_week, time_slots
from ScreenManager import ScreenManager
from UserControl.sidebar import create_sidebar

class TimetableApp:
    def __init__(self, root, coordinator_id):
        self.manual_timetable = {}
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
            command=self.show_export_options, 
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

        def update_discipline_options(event):
            selected_class = class_var.get()
            disciplines = self.get_lab_disciplines_for_class(selected_class)
            discipline_dropdown['values'] = disciplines
            discipline_var.set("")

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
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        disciplines = get_disciplines(self.coordinator_id)
        teachers = get_teacher_data(self.coordinator_id)
        teacher_limits = get_teacher_limits(self.coordinator_id)

        classes = self.get_filtered_classes()
        if not classes:
            print("⚠️ Nenhuma turma encontrada para este coordenador.")
            return {}

        timetable = {
            cls: {day: [['', ''] for _ in time_slots] for day in days_of_week}
            for cls in classes
        }

        timetable_entries = {cls: [] for cls in classes}
        availability_per_teacher = get_teacher_availability_for_timetable(teacher_limits, teachers)
        used_labs = {}

        for cls in classes:
            class_course = get_class_course(cls, self.coordinator_id)
            class_disciplines = [d for d in disciplines if d['course'] == class_course]

            discipline_hours = {d['name']: d['hours'] for d in class_disciplines}
            assigned_hours = {d['id']: 0 for d in class_disciplines}
            discipline_map = {d['id']: d for d in class_disciplines}
            
            cursor.execute("""
                SELECT discipline_id, division_count 
                FROM lab_division_config 
                WHERE class_id = ? AND coordinator_id = ?
            """, (get_class_id(cls, self.coordinator_id), self.coordinator_id))
            lab_division_map = {row[0]: row[1] for row in cursor.fetchall()}

            for day in days_of_week:
                for i, time_slot in enumerate(time_slots):
                    if time_slot == "20:25 - 20:45":
                        continue  # intervalo

                    inicio, termino = time_slot.split(" - ")
                    available_teachers_for_day = [
                        t for t in teachers if day in availability_per_teacher.get(t, [])
                        ]

                    possible_disciplines = [
                        d for d in class_disciplines if assigned_hours[d['id']] < discipline_hours[d['name']]
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
                        current_division = int(assigned_hours[discipline_id] / horas_por_divisao) + 1
                        if current_division > division_count:
                            continue  
                        if assigned_hours[discipline_id] >= horas_por_divisao * division_count:
                            continue

                        disciplina_label = f"{discipline_name}"
                        lab_name = get_available_lab(cursor, day, used_labs, self.coordinator_id)
                        turma_lab = lab_name if lab_name else ""

                        possible_teachers = [t for t in available_teachers_for_day if day not in self.teacher_allocations.get(t, set())]
                        teacher = random.choice(possible_teachers) if possible_teachers else ""

                        entry = {
                            "DIA": day,
                            "INÍCIO": inicio,
                            "TÉRMINO": termino,
                            "CÓDIGO": f"CMP{i+1:03}-L{current_division}",
                            "NOME": discipline_name,
                            "TURMA LAB": turma_lab,
                            "PROFESSOR": teacher,
                            "TEÓRICA": "",
                            "PRÁTICA": "X",
                            "ENCONTRO": ""
                        }

                    else:
                        disciplina_label = discipline_name
                        turma_lab = cls
                        teacher = random.choice(available_teachers_for_day) if available_teachers_for_day else ""

                    assigned_hours[discipline_id] += 1
                    self.teacher_allocations.setdefault(teacher, set()).add(day)
                    timetable[cls][day][i] = [disciplina_label, teacher]
                    turma_lab = "" if not requires_lab else cls
                    entry = {
                            "DIA": day,
                            "INÍCIO": inicio,
                            "TÉRMINO": termino,
                            "CÓDIGO": f"CMP{i+1:03}",
                            "NOME": disciplina_label,
                            "TURMA LAB": turma_lab,
                            "PROFESSOR": teacher,
                            "TEÓRICA": "X" if not requires_lab else "",
                            "PRÁTICA": "X" if requires_lab else "",
                            "ENCONTRO": ""
                        }

                    timetable_entries[cls].append(entry)

        conn.close()
        return timetable_entries

    def show_timetable(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        self.timetable = self.generate_timetable()
            
        for name, timetable_class in self.timetable.items():
            self.create_class_table(self.scroll_frame, name, timetable_class)

    def create_class_table(self, frame, class_name, timetable_class):
        week_order = {
            "Segunda": 0,
            "Terça": 1,
            "Quarta": 2,
            "Quinta": 3,
            "Sexta": 4,
        }

        timetable_class.sort(key=lambda x: (week_order.get(x["DIA"], 99), x["INÍCIO"]))

        class_frame = tk.Frame(frame)
        class_frame.pack(pady=10, fill="x", expand=True)

        title = tk.Label(
            class_frame,
            text=f"TURMA {class_name}",
            font=("Helvetica", 12, "bold"),
            pady=10
        )
        title.grid(row=0, column=0, columnspan=10)

        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(
            class_frame,
            text="",
            variable=var,
            command=lambda: self.select_grade(class_name, var)
        )
        checkbox.grid(row=0, column=10, padx=10)

        headers = ["DIA", "INÍCIO", "TÉRMINO", "CÓDIGO", "NOME", "TURMA LAB", "PROFESSOR", "TEÓRICA", "PRÁTICA", "ENCONTRO"]

        # Cabeçalhos
        for col, header in enumerate(headers):
            label = tk.Label(
                class_frame,
                text=header,
                font=("Helvetica", 10, "bold"),
                relief="ridge",
                borderwidth=1,
                width=14,
                bg="#F5F5F5"
            )
            label.grid(row=1, column=col, sticky="nsew")

        row = 2
        i = 0
        while i < len(timetable_class):
            current = timetable_class[i]
            day = current["DIA"]

            rowspan = 1
            for j in range(i + 1, len(timetable_class)):
                if timetable_class[j]["DIA"] == day:
                    rowspan += 1
                else:
                    break

            day_label = tk.Label(
                class_frame,
                text=day,
                font=("Helvetica", 9),
                relief="ridge",
                borderwidth=1
            )
            day_label.grid(row=row, column=0, rowspan=rowspan, sticky="nsew")

            # Restante das colunas
            for k in range(rowspan):
                entry = timetable_class[i + k]
                for col_idx, header in enumerate(headers[1:], start=1):
                    value = entry.get(header, "")
                    label = tk.Label(
                        class_frame,
                        text=value,
                        font=("Helvetica", 9),
                        relief="ridge",
                        borderwidth=1
                    )
                    label.grid(row=row + k, column=col_idx, sticky="nsew")

            i += rowspan
            row += rowspan


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
            

    def show_export_options(self):
        if not self.selected_grades:
            messagebox.showwarning("Aviso", "Nenhuma grade selecionada para download.")
            return
        
        option_window = tk.Toplevel(self.root)
        option_window.title("Escolher formato de exportação")
        option_window.geometry("300x150")
        option_window.grab_set() 

        excel_var = tk.BooleanVar(value=True)
        pdf_var = tk.BooleanVar(value=False)

        tk.Checkbutton(option_window, text="Exportar para Excel (.xlsx)", variable=excel_var).pack(pady=5)
        tk.Checkbutton(option_window, text="Exportar para PDF (.pdf)", variable=pdf_var).pack(pady=5)

        def start_export():
            export_excel = excel_var.get()
            export_pdf = pdf_var.get()
            option_window.destroy()
            self.download_grade(export_excel, export_pdf)

        tk.Button(option_window, text="Exportar", command=start_export).pack(pady=10)

    DB_NAME = "schedule.db"

    def download_grade(self, export_excel=True, export_pdf=False):
        if not self.selected_grades:
            messagebox.showwarning("Aviso", "Nenhuma grade selecionada para download.")
            return

        for grade_name in self.selected_grades:
            dir_path = filedialog.askdirectory(title="Escolha uma pasta para salvar os arquivos")
            if not dir_path:
                continue

            entries = self.manual_timetable.get(grade_name) or self.timetable.get(grade_name, [])
            headers = ["DIA", "INÍCIO", "TÉRMINO", "CÓDIGO", "NOME", "TURMA LAB", "PROFESSOR", "TEÓRICA", "PRÁTICA", "ENCONTRO"]

            grade_content = f"Grade de {grade_name}\n"
            grade_content += "\t".join(headers) + "\n"
            for entry in entries:
                row = "\t".join([str(entry.get(h, "")) for h in headers])
                grade_content += row + "\n"
            grade_content += "\n" + "=" * 30 + "\n"

            # Exporta para Excel
            if export_excel:
                excel_path = os.path.join(dir_path, f"{grade_name}.xlsx")
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = grade_name[:31]
                ws.append(headers)
                for entry in entries:
                    ws.append([entry.get(h, "") for h in headers])
                for col in range(1, len(headers) + 1):
                    cell = ws.cell(row=1, column=col)
                    cell.font = Font(bold=True)
                    cell.alignment = Alignment(horizontal="center")
                    max_length = max(len(str(cell.value)) for cell in ws[get_column_letter(col)])
                    ws.column_dimensions[get_column_letter(col)].width = max_length + 2
                wb.save(excel_path)
                print(f"✅ Excel salvo: {excel_path}")

            # Exporta para PDF
            if export_pdf:
                pdf_path = os.path.join(dir_path, f"{grade_name}.pdf")
                c = canvas.Canvas(pdf_path, pagesize=A4)
                width, height = A4
                y = height - 50
                c.setFont("Helvetica-Bold", 14)
                c.drawString(50, y, f"Grade de {grade_name}")
                y -= 30
                c.setFont("Helvetica", 10)
                for entry in entries:
                    line = " | ".join([f"{h}: {entry.get(h, '')}" for h in headers])
                    c.drawString(50, y, line[:180])
                    y -= 15
                    if y < 50:
                        c.showPage()
                        y = height - 50
                c.save()
                print(f"📄 PDF salvo: {pdf_path}")

            # Salva no banco
            conn = sqlite3.connect(self.DB_NAME)
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO saved_grades (name, content, file_path, coordinator_id)
            VALUES (?, ?, ?, ?)
            """, (grade_name, grade_content, dir_path, self.coordinator_id))
            conn.commit()
            conn.close()

        messagebox.showinfo("Sucesso", "Exportação concluída e grades salvas no banco!")

    def export_timetable_to_excel(self, timetable, filename="horario_gerado.xlsx"):
            wb = openpyxl.Workbook()
            wb.remove(wb.active)

            for cls, entries in timetable.items():
                ws = wb.create_sheet(title=cls[:31])

                headers = ["DIA", "INÍCIO", "TÉRMINO", "CÓDIGO", "NOME", "TURMA LAB", "PROFESSOR", "TEÓRICA", "PRÁTICA", "ENCONTRO"]
                ws.append(headers)

                for entry in entries:
                    ws.append([
                        entry.get("DIA", ""),
                        entry.get("INÍCIO", ""),
                        entry.get("TÉRMINO", ""),
                        entry.get("CÓDIGO", ""),
                        entry.get("NOME", ""),
                        entry.get("TURMA LAB", ""),
                        entry.get("PROFESSOR", ""),
                        entry.get("TEÓRICA", ""),
                        entry.get("PRÁTICA", ""),
                        entry.get("ENCONTRO", "")
                    ])

                for col in range(1, len(headers) + 1):
                    cell = ws.cell(row=1, column=col)
                    cell.font = Font(bold=True)
                    cell.alignment = Alignment(horizontal="center")
                    max_length = max(len(str(c.value)) if c.value else 0 for c in ws[get_column_letter(col)])
                    ws.column_dimensions[get_column_letter(col)].width = max_length + 2

            wb.save(filename)
            print(f"✅ Arquivo exportado: {filename}")


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
        manual_schedule_window.geometry("800x600")

        class_label = tk.Label(manual_schedule_window, text="Escolha a Turma:")
        class_label.pack(pady=8)

        classes = self.get_filtered_classes()
        class_var = tk.StringVar()
        class_select = ttk.Combobox(manual_schedule_window, textvariable=class_var, values=classes, state="readonly")
        class_select.pack(pady=8)

        table_frame = tk.Frame(manual_schedule_window)
        table_frame.pack(pady=10, fill="both", expand=True)

        discipline_data = get_disciplines(self.coordinator_id)
        teacher_data = get_teacher_data(self.coordinator_id)
        teachers = list(set(teacher_data))
        entries = []

        def load_schedule_table(event=None):
            for widget in table_frame.winfo_children():
                widget.destroy()
            selected_class = class_var.get()
            class_course = get_class_course(selected_class, self.coordinator_id)
            class_disciplines = [d for d in discipline_data if d['course'] == class_course]

            tk.Label(table_frame, text="DIA").grid(row=0, column=0)
            tk.Label(table_frame, text="HORÁRIO").grid(row=0, column=1)
            tk.Label(table_frame, text="DISCIPLINA").grid(row=0, column=2)
            tk.Label(table_frame, text="PROFESSOR").grid(row=0, column=3)

            row_idx = 1
            entries.clear()

            for day in days_of_week:
                for slot in time_slots:
                    if slot == "20:25 - 20:45":
                        continue

                    tk.Label(table_frame, text=day).grid(row=row_idx, column=0)
                    tk.Label(table_frame, text=slot).grid(row=row_idx, column=1)

                    discipline_var = tk.StringVar()
                    discipline_cb = ttk.Combobox(table_frame, textvariable=discipline_var, values=[d["name"] for d in class_disciplines])
                    discipline_cb.grid(row=row_idx, column=2)

                    teacher_var = tk.StringVar()
                    teacher_cb = ttk.Combobox(table_frame, textvariable=teacher_var, values=teachers)
                    teacher_cb.grid(row=row_idx, column=3)

                    entries.append({
                        "day": day,
                        "slot": slot,
                        "discipline_var": discipline_var,
                        "teacher_var": teacher_var
                    })

                    row_idx += 1

        class_select.bind("<<ComboboxSelected>>", load_schedule_table)

        def save_manual_schedule():
                selected_class = class_var.get()
                if not selected_class:
                    messagebox.showwarning("Aviso", "Selecione uma turma.")
                    return

                schedule = []
                used_slots = set()
                teacher_usage = {}

                for entry in entries:
                    day = entry["day"]
                    slot = entry["slot"]
                    discipline = entry["discipline_var"].get()
                    teacher = entry["teacher_var"].get()

                    if not discipline or not teacher:
                        continue

                    key = (day, slot)
                    if key in used_slots:
                        messagebox.showerror("Erro", f"Conflito de horário detectado: {day}, {slot}")
                        return

                    if (teacher, day, slot) in teacher_usage:
                        messagebox.showerror("Erro", f"Professor {teacher} já está alocado em {day} às {slot}.")
                        return

                    used_slots.add(key)
                    teacher_usage[(teacher, day, slot)] = True

                    discipline_obj = next((d for d in discipline_data if d["name"] == discipline), None)
                    pratica = discipline_obj.get("requires_laboratory", False) if discipline_obj else False

                    schedule.append({
                        "DIA": day,
                        "INÍCIO": slot.split(" - ")[0],
                        "TÉRMINO": slot.split(" - ")[1],
                        "CÓDIGO": "",
                        "NOME": discipline,
                        "TURMA LAB": selected_class if pratica else "",
                        "PROFESSOR": teacher,
                        "TEÓRICA": "" if pratica else "X",
                        "PRÁTICA": "X" if pratica else "",
                        "ENCONTRO": ""
                    })

                grade_name = f"{selected_class}_MANUAL"
                self.manual_timetable[grade_name] = schedule
                self.selected_grades = [grade_name]

                manual_schedule_window.destroy()
                self.show_export_options()


        save_button = tk.Button(manual_schedule_window, text="Salvar Grade", command=save_manual_schedule, bg="#A0D6B4")
        save_button.pack(pady=10)

        lab_config_button = tk.Button(manual_schedule_window, text="Configurar Laboratórios", command=self.open_lab_config_window, bg="#FFD580")
        lab_config_button.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimetableApp(root)
    root.mainloop()
