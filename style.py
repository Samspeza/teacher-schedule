# style.py
import tkinter as tk
# Cores
BACKGROUND_COLOR = "#F4F6F9"
BUTTON_COLOR = "#00796B"
BUTTON_TEXT_COLOR = "white"
LABEL_COLOR = "#B2DFDB"
TEXT_COLOR = "black"
WHITE_COLOR = "#FFFFFF"

# Fontes
HEADER_FONT = ("Arial", 18, "bold")
LABEL_FONT = ("Arial", 12, "bold")
TIME_SLOT_FONT = ("Arial", 12)
TEACHER_FONT = ("Arial", 10)

def style_tkinter_widgets(root):
    root.config(bg="#f5f5f5")
    root.geometry("1200x600")
    
    def style_frame(frame):
        frame.config(bg="#ffffff", relief="solid", borderwidth=1)
        
    def style_label(label, font_size=12, font_weight="normal", bg_color="#f5f5f5", fg_color="black"):
        label.config(font=("Arial", font_size, font_weight), bg=bg_color, fg=fg_color)
    
    return style_frame, style_label

def style_tkinter_widgets(root):
    root.config(bg="#f5f5f5")
    root.geometry("1200x600")
    
    def style_frame(frame):
        frame.config(bg="#ffffff", relief="solid", borderwidth=1)
        
    def style_label(label, font_size=12, font_weight="normal", bg_color="#f5f5f5", fg_color="black"):
        label.config(font=("Arial", font_size, font_weight), bg=bg_color, fg=fg_color)
    
    return style_frame, style_label

def display_timetable_gui(timetables, days_of_week, time_slots, teachers):
    root = tk.Tk()
    root.title("Grade de Aulas")
    
    style_frame, style_label = style_tkinter_widgets(root)

    canvas = tk.Canvas(root, bg="#F4F6F9")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.config(yscrollcommand=scrollbar.set)

    timetable_frame = tk.Frame(canvas, bg="#F4F6F9")
    canvas.create_window((0, 0), window=timetable_frame, anchor="nw")

    def create_class_table(name, timetable_class):
        frame = tk.Frame(timetable_frame, bg="#ffffff", relief="flat", borderwidth=0)
        frame.pack(padx=20, pady=20, fill="x", expand=True)
        style_frame(frame)

        label = tk.Label(frame, text=f"Grade para {name}", font=("Arial", 18, "bold"), bg="#00796B", fg="white")
        style_label(label, font_size=18, font_weight="bold", bg_color="#00796B", fg_color="white")
        label.grid(row=0, column=0, columnspan=len(days_of_week) + 1, pady=10)

        for i, day in enumerate(days_of_week):
            label = tk.Label(frame, text=day, font=("Arial", 12, "bold"), bg="#00796B", fg="white")
            style_label(label, font_size=12, font_weight="bold", bg_color="#00796B", fg_color="white")
            label.grid(row=1, column=i+1, padx=10, pady=10)

        for row, time_slot in enumerate(time_slots, start=2):
            label = tk.Label(frame, text=time_slot, font=("Arial", 12), bg="#B2DFDB", fg="black")
            style_label(label, font_size=12, font_weight="normal", bg_color="#B2DFDB", fg_color="black")
            label.grid(row=row, column=0, padx=15, pady=5)

            for col, day in enumerate(days_of_week, start=1):
                teacher = timetable_class[day].get(time_slot, None)
                teacher_label = tk.Label(frame, text=teacher, font=("Arial", 10), bg="#FFFFFF", fg="black")
                style_label(teacher_label, font_size=10, font_weight="normal", bg_color="#FFFFFF", fg_color="black")
                teacher_label.grid(row=row, column=col, padx=10, pady=5)

    def update_timetable(timetable):
        for widget in timetable_frame.winfo_children():
            widget.destroy()

        for name, timetable_class in timetable.items():
            create_class_table(name, timetable_class)

        timetable_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    update_timetable(timetables)
    root.mainloop()
