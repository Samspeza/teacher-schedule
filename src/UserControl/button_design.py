import tkinter as tk
from tkinter import PhotoImage
import os

BACKGROUND_COLOR = "#f0f0f0"

def load_icons():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icons_dir = os.path.join("teacher-schedule", "icons")

    print(f"Ícones localizados em: {icons_dir}")  

    try:
        save_icon_path = os.path.join(icons_dir, "salvar.png")
        if not os.path.exists(save_icon_path):
            print(f"Arquivo não encontrado: {save_icon_path}")
        
        save_icon = PhotoImage(file=save_icon_path).subsample(20, 20)

        cancel_icon_path = os.path.join(icons_dir, "cancel.png")
        if not os.path.exists(cancel_icon_path):
            print(f"Arquivo não encontrado: {cancel_icon_path}")

        cancel_icon = PhotoImage(file=cancel_icon_path).subsample(20, 20)

        list_icon_path = os.path.join(icons_dir, "list.png")
        if not os.path.exists(list_icon_path):
            print(f"Arquivo não encontrado: {list_icon_path}")
        
        list_icon = PhotoImage(file=list_icon_path).subsample(20, 20)

        edit_icon_path = os.path.join(icons_dir, "edit.png")
        if not os.path.exists(edit_icon_path):
            print(f"Arquivo não encontrado: {edit_icon_path}")
        
        edit_icon = PhotoImage(file=edit_icon_path).subsample(20, 20)

        delete_icon_path = os.path.join(icons_dir, "delete.png")
        if not os.path.exists(delete_icon_path):
            print(f"Arquivo não encontrado: {delete_icon_path}")
        
        delete_icon = PhotoImage(file=delete_icon_path).subsample(20, 20)

        create_icon_path = os.path.join(icons_dir, "mais.png")
        if not os.path.exists(create_icon_path):
            print(f"Arquivo não encontrado: {create_icon_path}")
        
        create_icon = PhotoImage(file=create_icon_path).subsample(20, 20)

        download_icon_path = os.path.join(icons_dir, "download.png")
        if not os.path.exists(download_icon_path):
            print(f"Arquivo não encontrado: {download_icon_path}")
        
        download_icon = PhotoImage(file=download_icon_path).subsample(20, 20)

        return {
            "save": save_icon,
            "cancel": cancel_icon,
            "list": list_icon,
            "edit": edit_icon,
            "delete": delete_icon,
            "create": create_icon,
            "download": download_icon
        }

    except Exception as e:
        print(f"Erro ao carregar ícones: {e}")
        return {}


def create_action_buttons(action_frame, commands):
    icons = load_icons()

    create_button = tk.Button(
        action_frame,
        image=icons.get("create"),
        command=commands["create"],
        padx=8,
        pady=4,
        borderwidth=0,
        relief="flat",
        highlightthickness=0,
        activebackground=BACKGROUND_COLOR
    )
    create_button.pack(side="left", padx=8)

    list_button = tk.Button(
        action_frame,
        image=icons.get("list"),
        command=commands["show_timetable"],
        padx=8,
        pady=4,
        borderwidth=0,
        relief="flat",
        highlightthickness=0,
        activebackground=BACKGROUND_COLOR
    )
    list_button.pack(side="left", padx=8)

    edit_button = tk.Button(
        action_frame,
        image=icons.get("edit"),
        command=commands["edit_teacher"],
        state="disabled",
        padx=8,
        pady=4,
        borderwidth=0,
        relief="flat",
        highlightthickness=0,
        activebackground=BACKGROUND_COLOR
    )
    edit_button.pack(side="left", padx=8)

    save_button = tk.Button(
        action_frame,
        image=icons.get("save"),
        command=commands["save_changes"],
        state="disabled",
        padx=8,
        pady=4,
        borderwidth=0,
        relief="flat",
        highlightthickness=0,
        activebackground=BACKGROUND_COLOR
    )
    save_button.pack(side="left", padx=8)

    cancel_button = tk.Button(
        action_frame,
        image=icons.get("cancel"),
        command=commands["cancel_edit"],
        state="disabled",
        padx=8,
        pady=4,
        borderwidth=0,
        relief="flat",
        highlightthickness=0,
        activebackground=BACKGROUND_COLOR
    )
    cancel_button.pack(side="left", padx=8)

    delete_button = tk.Button(
        action_frame,
        image=icons.get("delete"),
        command=commands["confirm_delete_schedule"],
        state="disabled",
        padx=8,
        pady=4,
        borderwidth=0,
        relief="flat",
        highlightthickness=0,
    )
    delete_button.pack(side="left", padx=8)

    download_button = tk.Button(
        action_frame,
        image=icons.get("download"),
        command=commands["download_grade"],
        state="disabled",
        padx=8,
        pady=4,
        borderwidth=0,
        relief="flat",
        highlightthickness=0,
    )
    download_button.pack(side="left", padx=8)

    
