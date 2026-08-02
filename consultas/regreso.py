import tkinter as tk
from tema import *
from consultas.inicio import inicio_a

def regresar(root, container):
    tk.Frame(container, height=10, bg=BG).pack()
    tk.Button(
        container,
        text="←",
        bg=BG,
        fg=TXT,
        relief="flat",
        activebackground=BG,
        activeforeground=TXT,
        font=(FUENTE, 14, "bold"),
        command=lambda: inicio_a(root, container)
    ).pack(anchor="w", padx=10)
