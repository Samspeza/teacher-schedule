import tkinter as tk
from tkinter import ttk
import random
from tkinter import PhotoImage
from tkinter.messagebox import askyesno
from style import *
from config import teachers, teacher_limits, classes, days_of_week, time_slots

class TimetableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciamento de Grade de Aulas")
        self.root.geometry("650x600")
        self.root.config(bg=BACKGROUND_COLOR)
        self.selected_cell = None
        self.teacher_allocations = {teacher: set() for teacher in teachers}
        
        self.setup_ui()
    
    def setup_ui(self):
        title_label = tk.Label(self.root, text="Gerenciamento de Grade de Aulas", font=HEADER_FONT, bg=HEADER_COLOR, fg=TEXT_COLOR)
        title_label.pack(pady=10)
        
        self.button_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        self.button_frame.pack(pady=10)
        
        self.save_icon = PhotoImage(file="icons/salvar.png").subsample(20, 20)  
        self.cancel_icon = PhotoImage(file="icons/cancel.png").subsample(20, 20)  
        
        self.list_icon = PhotoImage(file="icons/list.png").subsample(20, 20)  
        self.edit_icon = PhotoImage(file="icons/edit.png").subsample(20, 20)  
        self.delete_icon = PhotoImage(file="icons/delete.png").subsample(20, 20)  
        
        self.list_button = tk.Button(self.button_frame, image=self.list_icon, command=self.show_timetable, padx=8, pady=4)
        self.list_button.pack(side="left", padx=8)
        
        self.edit_button = tk.Button(self.button_frame, image=self.edit_icon, command=self.edit_teacher, state="disabled", padx=8, pady=4)
        self.edit_button.pack(side="left", padx=8)
        
        self.save_button = tk.Button(self.button_frame, image=self.save_icon, command=self.save_changes, state="disabled", padx=8, pady=4)
        self.save_button.pack(side="left", padx=8)

        self.cancel_button = tk.Button(self.button_frame, image=self.cancel_icon, command=self.cancel_edit, state="disabled", padx=8, pady=4)
        self.cancel_button.pack(side="left", padx=8)
        
        self.delete_button = tk.Button(self.button_frame, image=self.delete_icon, command=self.confirm_delete_schedule, state="disabled", padx=8, pady=4)
        self.delete_button.pack(side="left", padx=8)
        
        self.timetable_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
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
    
    def generate_timetable(self):
        timetable = {cls: {day: {time_slot: None for time_slot in time_slots} for day in days_of_week} for cls in classes}
    
        for cls in classes:
            for day in days_of_week:
                previous_teacher = None
                for i, time_slot in enumerate(time_slots):
                    available_teachers = [
                        teacher for teacher in teachers
                        if teacher not in teacher_limits or len(self.teacher_allocations[teacher]) < teacher_limits.get(teacher, float('inf'))
                    ]
    
                    if time_slot == "20:25 - 20:45": 
                        teacher = "INTERVALO"
                    elif not available_teachers:
                        teacher = "[SEM PROFESSOR]"
                    else:
                        if previous_teacher and previous_teacher in available_teachers and random.random() < 0.2:
                            teacher = previous_teacher
                        else:
                            teacher = random.choice([t for t in available_teachers if t != previous_teacher] or available_teachers)
                            self.teacher_allocations[teacher].add(day)
                    
                    timetable[cls][day][time_slot] = teacher
                    previous_teacher = teacher
        return timetable
    
    def show_timetable(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        self.timetable = self.generate_timetable()
        
        for name, timetable_class in self.timetable.items():
            self.create_class_table(self.scroll_frame, name, timetable_class)
    
    def create_class_table(self, parent, name, timetable_class):
        frame = tk.Frame(parent, bg=WHITE_COLOR, relief="solid", borderwidth=1)
        frame.pack(padx=15, pady=10, fill="x", expand=True)
        
        label = tk.Label(frame, text=f"Grade para {name}", font=HEADER_FONT, bg=HEADER_COLOR, fg=TEXT_COLOR)
        label.grid(row=0, column=0, columnspan=len(days_of_week) + 1, pady=5)
        
        for i, day in enumerate(days_of_week):
            tk.Label(frame, text=day, font=LABEL_FONT, bg=HEADER_COLOR, fg=TEXT_COLOR).grid(row=1, column=i+1, padx=6, pady=6)
        
        for row, time_slot in enumerate(time_slots, start=2):
            tk.Label(frame, text=time_slot, font=TIME_SLOT_FONT, bg=LABEL_COLOR, fg=TEXT_COLOR).grid(row=row, column=0, padx=10, pady=3)
            for col, day in enumerate(days_of_week, start=1):
                teacher = timetable_class[day].get(time_slot, None)
                cell_label = tk.Label(frame, text=teacher, font=TEACHER_FONT, bg=WHITE_COLOR, fg=TEXT_COLOR, padx=8, pady=4, relief="groove", borderwidth=1)
                cell_label.grid(row=row, column=col, padx=6, pady=3)
                cell_label.bind("<Button-1>", lambda e, d=day, t=time_slot, l=cell_label: self.select_cell(d, t, l))
    
    def select_cell(self, day, time_slot, label):
        if self.selected_cell:
            self.selected_cell.config(bg=WHITE_COLOR)
        
        self.selected_cell = label
        self.selected_cell.config(bg=LABEL_COLOR)
        
        self.original_teacher = self.selected_cell.cget("text")  
        self.edit_button.config(state="normal")
        self.save_button.config(state="normal")
        self.cancel_button.config(state="normal")
        self.delete_button.config(state="normal")
    
    def edit_teacher(self):
        if not self.selected_cell:
            return
        
        self.original_teacher = self.selected_cell.cget("text") 
        self.open_teacher_modal()
    
    def open_teacher_modal(self):
        modal_window = tk.Toplevel(self.root)
        modal_window.title("Escolher Novo Professor")
        
        label = tk.Label(modal_window, text="Selecione um novo professor:")
        label.pack(pady=8)
        
        teacher_select = ttk.Combobox(modal_window, values=list(teachers.keys()))  
        teacher_select.set(self.selected_cell.cget("text"))  

        teacher_select.pack(pady=8)
        
        def save_teacher():
            new_teacher = teacher_select.get()
            self.selected_cell.config(text=new_teacher)  
            modal_window.destroy()
            self.save_button.config(state="disabled")
            self.cancel_button.config(state="disabled")
        
        def cancel():
            modal_window.destroy()
            self.selected_cell.config(text=self.original_teacher)  
        
        self.save_button.config(command=save_teacher, state="normal")
        self.cancel_button.config(command=cancel, state="normal")
    
    def save_changes(self):
        if self.selected_cell:
            new_teacher = self.selected_cell.cget("text")  
            self.selected_cell.config(text=new_teacher) 
        
            self.save_button.config(state="disabled")
            self.cancel_button.config(state="disabled")
    
    def cancel_edit(self):
        if self.selected_cell:
            self.selected_cell.config(text=self.original_teacher)  
        
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

if __name__ == "__main__":
    root = tk.Tk()
    app = TimetableApp(root)
    root.mainloop()
