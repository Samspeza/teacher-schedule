import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
import os

class SavedGradesApp:
    def __init__(self, root, coordinator_id):
        self.root = root
        self.coordinator_id = coordinator_id
        self.root.title("Grades Salvas")
        self.root.geometry("1175x900")
        self.root.configure(bg="#F0F2F5")

        # Sidebar
        self.sidebar = self.create_sidebar()

        # Main Frame
        main_frame = tk.Frame(self.root, bg="#F0F2F5")
        main_frame.pack(side="left", fill="both", expand=True)

        # Header
        header_frame = tk.Frame(main_frame, bg="#F0F2F5", height=70)
        header_frame.pack(fill="x", padx=15, pady=10)

        tk.Label(header_frame, text="📚 Grades Salvas", font=("Segoe UI", 16, "bold"),
                 bg="#F8F8F8", fg="#2A72C3").pack(side="left", padx=10)

        # Table Frame
        table_frame = tk.Frame(main_frame, bg="#FFFFFF")
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        columns = ("ID", "Nome da Grade", "Conteúdo", "Caminho do Arquivo")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200, anchor="center")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.pack(fill="both", expand=True)

        # Pagination Controls
        pagination_frame = tk.Frame(main_frame, bg="#F0F2F5")
        pagination_frame.pack(fill="x", pady=(0, 10))

        self.page_num = 1
        self.total_pages = 1
        self.items_per_page = 25

        self.prev_btn = ttk.Button(pagination_frame, text="<<", command=lambda: self.change_page(self.page_num - 1))
        self.prev_btn.pack(side="left", padx=2)

        self.page_label = ttk.Label(pagination_frame, text=f"Página {self.page_num} de {self.total_pages}")
        self.page_label.pack(side="left", padx=10)

        self.next_btn = ttk.Button(pagination_frame, text=">>", command=lambda: self.change_page(self.page_num + 1))
        self.next_btn.pack(side="left", padx=2)

        # Load saved grades
        self.load_saved_grades()

        # Bind double-click to open details
        self.tree.bind("<Double-1>", self.open_grade_details)

    def create_sidebar(self):
        sidebar_frame = tk.Frame(self.root, bg="#007BBD", width=100, height=700)
        sidebar_frame.pack(side="left", fill="y")

        self.icon_label = tk.Label(sidebar_frame, text="🎓", font=("Arial", 40), bg="#007BBD", fg="#FFFFFF", cursor="hand2")
        self.icon_label.pack(side="top", padx=20, pady=20)
        self.icon_label.bind("<Button-1>", self.show_home_screen)

        return sidebar_frame

    def show_home_screen(self, event=None):
        from ScreenManager import ScreenManager
        self.root.destroy()
        home_root = tk.Tk()
        app = ScreenManager(home_root, self.coordinator_id)
        home_root.mainloop()

    def load_saved_grades(self):
        # Load saved grades from the database
        conn = sqlite3.connect('schedule.db')
        cursor = conn.cursor()

        # Get the total count of saved grades
        cursor.execute("SELECT COUNT(*) FROM saved_grades WHERE coordinator_id = ?", (self.coordinator_id,))
        total_items = cursor.fetchone()[0]
        conn.close()

        # Calculate the total pages
        self.total_pages = (total_items // self.items_per_page) + (1 if total_items % self.items_per_page else 0)
        self.page_label.config(text=f"Página {self.page_num} de {self.total_pages}")

        # Load the grades from the database with pagination
        conn = sqlite3.connect('schedule.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, content, file_path
            FROM saved_grades
            WHERE coordinator_id = ?
            LIMIT ? OFFSET ?
        """, (self.coordinator_id, self.items_per_page, (self.page_num - 1) * self.items_per_page))
        saved_grades = cursor.fetchall()
        conn.close()

        # Insert grades into the treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        for grade in saved_grades:
            self.tree.insert("", "end", values=grade)

    def change_page(self, page_num):
        if 1 <= page_num <= self.total_pages:
            self.page_num = page_num
            self.load_saved_grades()

    def save_grade_to_file(self, grade_id, grade_name, grade_content):
        # Open file dialog to choose save location
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(grade_content)
                messagebox.showinfo("Sucesso", f"Grade salva com sucesso em {file_path}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar o arquivo: {str(e)}")

    def save_to_pdf(self, grade_name, grade_content):
        # Save to PDF
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            try:
                c = canvas.Canvas(file_path, pagesize=letter)
                c.drawString(100, 750, f"Grade: {grade_name}")
                c.drawString(100, 730, f"Conteúdo: {grade_content}")
                c.save()
                messagebox.showinfo("Sucesso", f"Grade salva como PDF em {file_path}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar PDF: {str(e)}")

    def save_to_excel(self, grade_name, grade_content):
        # Save to Excel
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            try:
                df = pd.DataFrame({"Grade": [grade_name], "Conteúdo": [grade_content]})
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Sucesso", f"Grade salva como Excel em {file_path}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar Excel: {str(e)}")

    def delete_grade(self, grade_id):
        # Delete the grade from the database
        conn = sqlite3.connect('schedule.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM saved_grades WHERE id = ?", (grade_id,))
        conn.commit()
        conn.close()
        self.load_saved_grades()

    def open_grade_details(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        grade_id = self.tree.item(selected_item[0], "values")[0]
        grade_name = self.tree.item(selected_item[0], "values")[1]
        grade_content = self.tree.item(selected_item[0], "values")[2]

        details_window = tk.Toplevel(self.root)
        details_window.title(f"Detalhes da Grade - {grade_name}")
        details_window.geometry("600x400")

        text_box = tk.Text(details_window, wrap="word", height=15, width=70)
        text_box.insert(tk.END, f"Grade: {grade_name}\n\nConteúdo:\n{grade_content}")
        text_box.pack(padx=10, pady=10)

        # Buttons to save as PDF or Excel
        save_pdf_button = ttk.Button(details_window, text="Salvar como PDF", command=lambda: self.save_to_pdf(grade_name, grade_content))
        save_pdf_button.pack(pady=10)

        save_excel_button = ttk.Button(details_window, text="Salvar como Excel", command=lambda: self.save_to_excel(grade_name, grade_content))
        save_excel_button.pack(pady=10)

# Running the App
if __name__ == "__main__":
    root = tk.Tk()
    app = SavedGradesApp(root, coordinator_id=1)  # Pass coordinator_id as needed
    root.mainloop()
