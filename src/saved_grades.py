import sqlite3
import tkinter as tk
import json
import os
from DbContext.database import DB_NAME
from DbContext.models import create_tables
import tkinter.messagebox as messagebox
from tkinter import PhotoImage
from UserControl.sidebar import create_sidebar

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

    file_name = f"grade_{grade_id}.json"
    file_path = os.path.join(os.getcwd(), "saved_grades", file_name)
    
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    
    with open(file_path, 'w') as file:
        json.dump(contents, file)

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
    
    cursor.execute("SELECT id, name, content, file_path FROM saved_grades")
    saved_grades = cursor.fetchall()
    
    conn.close()
    
    return saved_grades


def get_grade_by_name(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, content, file_path FROM saved_grades WHERE name = ?", (name,))
    grade = cursor.fetchone()
    
    conn.close()
    
    return grade


def delete_grade_by_name(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, file_path FROM saved_grades WHERE name = ?", (name,))
    grade = cursor.fetchone()

    if grade:
        grade_id, file_path = grade

        if file_path and os.path.exists(file_path):
            os.remove(file_path)

        cursor.execute("DELETE FROM saved_grades WHERE id = ?", (grade_id,))
        conn.commit()
    
    conn.close()


if __name__ == "__main__": 
    create_tables()  
    saved_root = tk.Tk()
    saved_app = SavedGradesApp(saved_root)
    saved_root.mainloop()
