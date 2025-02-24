import sqlite3
import tkinter as tk
import os
from DbContext.database import DB_NAME
from DbContext.models import create_tables
import tkinter.messagebox as messagebox
from tkinter import PhotoImage
from UserControl import config
from UserControl.sidebar import create_sidebar
from UserControl.config import days_of_week, time_slots
import re

class SavedGradesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grades Salvas")
        self.root.geometry("900x800")
        self.root.configure(bg="#F8F8F8")
        
        # Criar o sidebar
        self.sidebar = create_sidebar(self.root, self.show_home_screen, self.show_modules_screen, self.save_changes)
        
        # Contêiner principal
        content_frame = tk.Frame(self.root, bg="#F8F8F8")
        content_frame.pack(side="right", fill="both", expand=True)

        header_frame = tk.Frame(content_frame, bg="#F8F8F8", height=80)
        header_frame.pack(side="top", fill="x")
        
        self.icon_label = tk.Label(header_frame, text="🎓", font=("Arial", 40), bg="#F8F8F8", fg="#2A72C3")
        self.icon_label.pack(side="left", padx=20)
        
        self.menu_label = tk.Label(header_frame, text="GRADES SALVAS", font=("Arial", 16, "bold"), bg="#F8F8F8", fg="#2A72C3")
        self.menu_label.pack(side="left")
        
        self.saved_grades_listbox = tk.Listbox(content_frame, font=("Arial", 14), bg="#F8F8F8", fg="#2A72C3", selectmode=tk.SINGLE)
        self.saved_grades_listbox.pack(pady=20, padx=50, fill="both", expand=True)
        
        button_frame = tk.Frame(content_frame, bg="#F8F8F8")
        button_frame.pack(pady=10)

        self.re_save_button = tk.Button(button_frame, text="Salvar Novamente", font=("Arial", 12), bg="#2A72C3", fg="white", command=self.re_save_grade)
        self.re_save_button.pack(side="left", padx=10)

        self.delete_button = tk.Button(button_frame, text="Deletar Grade", font=("Arial", 12), bg="red", fg="white", command=self.delete_grade)
        self.delete_button.pack(side="left", padx=10)

        self.saved_grades_listbox.bind("<Double-1>", self.load_grade)  
        
        self.populate_saved_grades()
        
    def populate_saved_grades(self):
        self.saved_grades_listbox.delete(0, tk.END)
        saved_grades = get_saved_grades()  
        for grade in saved_grades:
            self.saved_grades_listbox.insert(tk.END, grade[1])  

    def re_save_grade(self):
        selected_index = self.saved_grades_listbox.curselection()
        if selected_index:
            selected_grade = self.saved_grades_listbox.get(selected_index)  
            grade = get_grade_by_name(selected_grade)
            if grade:
                grade_name = grade[1]  
                grade_contents = grade[2]  
                save_grade(grade_name, grade_contents)  
                messagebox.showinfo("Sucesso", f"Grade '{grade_name}' salva novamente!")
                self.saved_grades_listbox.insert(selected_index, grade_name)  

    def delete_grade(self):
        selected_index = self.saved_grades_listbox.curselection()
        if selected_index:
            selected_grade = self.saved_grades_listbox.get(selected_index)  
            confirm = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja deletar a grade '{selected_grade}'?")
            
            if confirm:
                delete_grade_by_name(selected_grade)
                self.populate_saved_grades()
                messagebox.showinfo("Sucesso", f"Grade '{selected_grade}' deletada com sucesso!")
        else:
            messagebox.showwarning("Aviso", "Selecione uma grade para deletar.")

    def teacher_exists(name):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM teachers WHERE name = ?", (name,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    import re

    @staticmethod
    def parse_grade_contents(line):
        """
        Processa cada linha do arquivo de grade de horários e extrai as informações de horários e professores.
        """
        line = line.strip()

        # Se a linha for um dia da semana, retorna como um marcador
        if line in ["Segunda:", "Terça:", "Quarta:", "Quinta:", "Sexta:"]:
            return "DAY", line[:-1]  # Remove os ":" e retorna o nome do dia

        if not line or "==============================" in line:
            return None  

        # Expressão para capturar o horário e o professor
        match = re.match(r"(\d{2}:\d{2} - \d{2}:\d{2}):\s*(.*)", line)
        if match:
            time_range = match.group(1)
            teacher_name = match.group(2).strip()

            # Se for intervalo, armazenamos explicitamente
            if teacher_name == "INTERVALO":
                return time_range, "INTERVALO"

            return time_range, teacher_name

        return None

    def extract_day_time(self, time_range):
        """
        Extrai o dia da semana e o horário do intervalo de tempo fornecido.
        """
        for day in config.days_of_week:
            for slot in config.time_slots:
                if time_range in slot:
                    return day, slot
        return None, None 

        
    def load_grade(self, event):
        """Carrega a grade salva ao dar um duplo clique."""
        selected_index = self.saved_grades_listbox.curselection()
        if selected_index:
            selected_grade = self.saved_grades_listbox.get(selected_index)
            print(f"Selecionado: {selected_grade}")

            grade = get_grade_by_name(selected_grade)  
            if not grade:
                messagebox.showerror("Erro", "Grade não encontrada no banco de dados.")
                return

            grade_name = grade[1]  
            grade_contents = grade[2].split("\n")  

            timetable_class = {}

            current_day = None  

            for line in grade_contents:
                parsed_data = self.parse_grade_contents(line)

                if parsed_data:
                    if parsed_data[0] == "DAY":  
                        current_day = parsed_data[1]  
                        timetable_class[current_day] = {}  
                    elif current_day and isinstance(parsed_data, tuple):
                        time_range, teacher_name = parsed_data
                        timetable_class[current_day][time_range] = teacher_name 

            print(f"Grade gerada: {timetable_class}")  
            self.generate_grade(grade_name, timetable_class)


    def generate_grade(self, grade_name, timetable_class):
        frame = tk.Frame(self.root, bg="#F8F8F8", relief="solid", borderwidth=1)
        frame.pack(padx=20, pady=10, fill="x", expand=True)

        header = tk.Frame(frame)
        header.grid(row=0, column=0, columnspan=5, sticky="ew")
        
        header_label = tk.Label(header, text=f"Grade para {grade_name}", font=("Arial", 16, "bold"), fg="#2A72C3")
        header_label.pack(side="left", padx=10, pady=5)
        
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(header, variable=var)
        checkbox.pack(side="right", padx=10, pady=5)
        
        tk.Label(frame, text="", font=("Arial", 12), fg="#2A72C3", relief="ridge", borderwidth=1).grid(row=1, column=0, padx=6, pady=6, sticky="nsew")
        
        for i, day in enumerate(days_of_week):
            day_label = tk.Label(frame, text=day, font=("Arial", 12), fg="#2A72C3", relief="ridge", borderwidth=1)
            day_label.grid(row=1, column=i+1, padx=6, pady=6, sticky="nsew")
        
        for row, time_slot in enumerate(time_slots, start=2):
            time_label = tk.Label(frame, text=time_slot, font=("Arial", 12), bg="#F8F8F8", fg="#2A72C3", relief="ridge", borderwidth=1)
            time_label.grid(row=row, column=0, padx=10, pady=3, sticky="nsew")

            for col, day in enumerate(days_of_week, start=1):
                teacher = timetable_class.get(day, {}).get(time_slot, "[SEM PROFESSOR]")
                cell_label = tk.Label(frame, text=teacher, font=("Arial", 12), bg="#FFFFFF", fg="#2A72C3", padx=8, pady=4, relief="groove", borderwidth=1)
                cell_label.grid(row=row, column=col, padx=6, pady=3, sticky="nsew")


    def show_home_screen(self):
        """Retorna à tela inicial."""
        from ScreenManager import ScreenManager  
        self.root.destroy()
        home_root = tk.Tk()
        app = ScreenManager(home_root)
        home_root.mainloop()

    def show_modules_screen(self):
        """Expande ou recolhe o painel de módulos."""
        if self.modules_frame.winfo_ismapped():
            self.modules_frame.pack_forget()  
        else:
            self.modules_frame.pack(pady=10, padx=10, fill="x")  

    def save_changes(self):
        if self.selected_cell:
            new_teacher = self.selected_cell.cget("text")  
            self.selected_cell.config(text=new_teacher) 
        
            self.save_button.config(state="disabled")
            self.cancel_button.config(state="disabled")


# Funções do banco de dados
def save_grade(name, contents):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO saved_grades (name, content, file_path)
    VALUES (?, ?, ?)
    """, (name, contents, ""))  
    
    conn.commit()
    
    grade_id = cursor.lastrowid

    file_name = f"grade_{grade_id}.txt"
    file_path = os.path.join(os.getcwd(), "saved_grades", file_name)
    
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    
    with open(file_path, 'w') as file:
        file.write(contents)

    cursor.execute("""
    UPDATE saved_grades
    SET file_path = ?
    WHERE id = ?
    """, (file_path, grade_id))
    
    conn.commit()
    conn.close()


def get_saved_grades():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM saved_grades")
    return cursor.fetchall()

def get_grade_by_name(grade_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM saved_grades WHERE name = ?", (grade_name,))
    return cursor.fetchone()

def delete_grade_by_name(grade_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT file_path FROM saved_grades WHERE name = ?", (grade_name,))
    file_path = cursor.fetchone()
    
    if file_path:
        if os.path.exists(file_path[0]):
            os.remove(file_path[0])
    
    cursor.execute("DELETE FROM saved_grades WHERE name = ?", (grade_name,))
    conn.commit()
    conn.close()

if __name__ == "__main__": 
    create_tables()  
    saved_root = tk.Tk()
    saved_app = SavedGradesApp(saved_root)
    saved_root.mainloop()
