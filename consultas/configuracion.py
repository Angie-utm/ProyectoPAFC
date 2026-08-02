import tkinter as tk
from bd import iniciar_bd
from tema import *

def conf(root, container, id_usuario):
    from consultas.inicio import inicio_a
    from consultas.lista_libros import barra_navegacion
    for w in container.winfo_children():
        w.destroy()

    tk.Frame(container, height=10, bg=BG).pack()
    tk.Button(
        container,
        text="✕  Cerrar Sesión",
        bg=BG,
        fg=TXT,
        relief="flat",
        activebackground=BG,
        activeforeground=TXT,
        font=(FUENTE, 10, "bold"),
        command=lambda: inicio_a(root, container),
    ).pack(anchor="e", padx=10, pady=(0, 10))

    barra_navegacion(container, root, container, id_usuario, 1)

    db = iniciar_bd()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (id_usuario,))
    users = cursor.fetchone()
    db.close()

    user_frame = tk.Frame(container, bg=CARD, padx=20, pady=15)
    user_frame.pack(padx=20, pady=10, fill="x")

    datos = [
        ("Nombre y apellido:", f"{users['nombre']} {users['apellido']}"),
        ("Usuario:", users['username']),
    ]
    for etiqueta, valor in datos:
        tk.Label(user_frame, text=etiqueta, bg=CARD, fg=TXT, font=(FUENTE, 11, "bold")).pack(anchor="w", pady=(5, 0))
        tk.Label(user_frame, text=valor, bg=CARD, fg=TXT, font=(FUENTE, 11), wraplength=300, justify="left").pack(anchor="w")

    tk.Frame(container, height=10, bg=BG).pack()
