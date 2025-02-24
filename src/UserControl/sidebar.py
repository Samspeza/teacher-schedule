import tkinter as tk
from tkinter import PhotoImage

def create_sidebar(root, show_home_screen, show_modules_screen, save_changes):
    sidebar_frame = tk.Frame(root, bg="#2A72C3", width=200)
    sidebar_frame.pack(side="left", fill="y")
    sidebar_frame.pack_propagate(False)
    
    graduation_button = tk.Button(
        sidebar_frame,
        text="🎓",
        command=show_home_screen,
        font=("Arial", 80),
        fg="white",
        bg="#2A72C3",
        borderwidth=0,
        relief="flat",
        highlightthickness=0
    )
    graduation_button.pack(pady=10)

    module_icon = PhotoImage(file="icons/list.png").subsample(15, 15)

    module_button = tk.Button(
        sidebar_frame,
        image=module_icon,
        text=" Módulos",
        font=("Arial", 12),
        fg="white",
        bg="#2A72C3",
        compound="left",
        borderwidth=0,
        relief="flat",
        anchor="w",
        padx=10,
        command=lambda: toggle_modules(modules_frame)
    )
    module_button.pack(pady=10, padx=10, fill="x")

    modules_frame = tk.Frame(sidebar_frame, bg="#1F5AA9")
    modules_frame.pack_forget() 

    save_grades_button = tk.Button(
        modules_frame,
        text="Salvar Grades",
        font=("Arial", 12),
        fg="white",
        bg="#1F5AA9",
        borderwidth=0,
        relief="flat",
        command=save_changes
    )
    save_grades_button.pack(fill="x")

    return sidebar_frame

def toggle_modules(modules_frame):
    if modules_frame.winfo_ismapped():  
        modules_frame.pack_forget()
    else: 
        modules_frame.pack(fill="x", padx=10)
