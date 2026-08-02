import tkinter as tk
from tkinter import ttk

BG = "#2a2a2a"
BG_SEC = "#1f1f1f"
CARD = "#333333"
TXT = "#FFFFFF"
ROJO = "#8B3A3A"
AZUL = "#A44A4A"
NEGRO = "#000000"
AMBER = "#7A2F2F"
FONDO_CAMPO = "#F5F5F5"

FUENTE = "Arial"


def aplicar_tema(root: tk.Tk) -> None:
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure("TButton", background=ROJO, foreground=NEGRO, bordercolor=ROJO)
    style.map("TButton", background=[("active", ROJO)], foreground=[("active", NEGRO)])

    style.configure("TCombobox", fieldbackground=FONDO_CAMPO, background=ROJO, foreground=NEGRO)
    style.map("TCombobox", background=[("active", ROJO)], foreground=[("active", NEGRO)])

    style.configure("TLabel", background=BG, foreground=TXT)
    style.configure("TFrame", background=BG)

    root.option_add("*Font", (FUENTE, 10))
