import tkinter as tk

def style_tkinter_widgets(root):
    root.config(bg="#f5f5f5")
    root.geometry("1200x600")
    
    def style_frame(frame):
        frame.config(bg="#ffffff", relief="solid", borderwidth=1)
    def style_label(label, font_size=12, font_weight="normal", bg_color="#f5f5f5", fg_color="black"):
        label.config(font=("Arial", font_size, font_weight), bg=bg_color, fg=fg_color)
    
    return style_frame, style_label
