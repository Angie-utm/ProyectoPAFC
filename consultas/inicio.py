import tkinter as tk
from PIL import Image, ImageTk
from tema import *
from consultas.iniciar_sesion import iniciar_sesion_a

def inicio_a(root, container):
    from consultas.registro import registro_usuario
    for w in container.winfo_children():
        w.destroy()

    tk.Frame(container, height=50, bg=BG).pack()

    try:
        img = Image.open("assets/rp.ico").convert("RGBA").resize((300, 200), Image.LANCZOS)
        logo = ImageTk.PhotoImage(img)
        lbl_logo = tk.Label(container, image=logo, bg=BG)
        lbl_logo.image = logo
        lbl_logo.pack(pady=(0, 20))
    except Exception:
        pass

    btn_login = tk.Button(
        container,
        text="Iniciar Sesión",
        width=20,
        height=2,
        bg=ROJO,
        fg=NEGRO,
        activebackground=ROJO,
        activeforeground=NEGRO,
        font=(FUENTE, 13, "bold"),
        command=lambda: iniciar_sesion_a(root, container),
    )
    btn_login.pack()

    tk.Label(container, text="O", bg=BG, fg=TXT, font=(FUENTE, 12)).pack(pady=10)

    btn_registro = tk.Button(
        container,
        text="Registrarse",
        width=20,
        height=2,
        bg=ROJO,
        fg=NEGRO,
        activebackground=ROJO,
        activeforeground=NEGRO,
        font=(FUENTE, 13, "bold"),
        command=lambda: registro_usuario(root, container),
    )
    btn_registro.pack()
