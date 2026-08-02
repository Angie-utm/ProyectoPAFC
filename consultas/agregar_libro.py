import tkinter as tk
from tkinter import messagebox
import mysql.connector
from bd import iniciar_bd
from tema import *

def agregar_libro(root, container, id_usuario):
    from consultas.lista_libros import show_dvds
    for w in container.winfo_children():
        w.destroy()
    tk.Label(
        container,
        text="Agregar Libro",
        bg=BG,
        fg=ROJO,
        font=(FUENTE,20,"bold")
    ).pack(pady=15)

    def crear_campo(texto):

        tk.Label(
            container,
            text=texto,
            bg=BG,
            fg=TXT,
            font=(FUENTE,11)
        ).pack()
        entry=tk.Entry(
            container,
            width=35,
            bg=FONDO_CAMPO,
            fg=NEGRO
        )
        entry.pack(pady=(2,10))
        return entry

    nombre=crear_campo("Nombre")
    autor=crear_campo("Autor")
    categoria=crear_campo("Categoría")

    def guardar():
        if (not nombre.get()
            or not autor.get()
            or not categoria.get()):
            messagebox.showerror(
                "Error",
                "Complete todos los campos."
            )
            return
        try:
            db=iniciar_bd()
            cursor=db.cursor()
            cursor.execute("""
                INSERT INTO libros
                (titulo,autor,categoria)
                VALUES (%s,%s,%s)""",
            (
                nombre.get(),
                autor.get(),
                categoria.get()
            ))
            db.commit()
            cursor.close()
            db.close()
            messagebox.showinfo(
                "Éxito",
                "Libro agregado correctamente."
            )
            show_dvds(root,container,id_usuario)

        except ValueError:
            messagebox.showerror(
                "Error",
                "La cantidad debe ser un número."
            )

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Error",
                err
            )

    tk.Button(
        container,
        text="Guardar",
        width=20,
        bg=ROJO,
        fg=NEGRO,
        activebackground=ROJO,
        activeforeground=NEGRO,
        font=(FUENTE,11,"bold"),
        command=guardar
    ).pack(pady=15)

    tk.Button(
        container,
        text="Cancelar",
        width=20,
        command=lambda: show_dvds(root,container,id_usuario)
    ).pack()