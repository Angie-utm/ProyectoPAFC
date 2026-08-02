import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import datetime
import mysql.connector

from bd import iniciar_bd
from tema import *


def agregar_renta(root, container, id_usuario, cantidad=1):

    from consultas.lista_libros import show_dvds

    for w in container.winfo_children():
        w.destroy()

    tk.Label(
        container,
        text="Agregar Renta",
        bg=BG,
        fg=ROJO,
        font=(FUENTE, 20, "bold")
    ).pack(pady=15)

    # Obtener libros

    db = iniciar_bd()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_libro,titulo
        FROM libros
        ORDER BY titulo
    """)

    libros = cursor.fetchall()

    opciones = []

    for libro in libros:
        opciones.append(f"{libro['id_libro']} - {libro['titulo']}")

    # Libro

    tk.Label(container, text="Libro", bg=BG, fg=TXT).pack()

    combo = ttk.Combobox(
        container,
        values=opciones,
        width=35,
        state="readonly"
    )
    combo.pack(pady=5)

    if opciones:
        combo.current(0)

    # Cedula

    tk.Label(container, text="Cédula", bg=BG, fg=TXT).pack()

    cedula = tk.Entry(container, width=35)
    cedula.pack(pady=5)

    # Cliente

    tk.Label(container, text="Cliente", bg=BG, fg=TXT).pack()

    cliente = tk.Entry(container, width=35)
    cliente.pack(pady=5)

    # Cantidad

    tk.Label(container, text="Cantidad", bg=BG, fg=TXT).pack()

    entrada_cantidad = tk.Entry(container, width=10)
    entrada_cantidad.insert(0, "1")
    entrada_cantidad.pack(pady=5)

    # Fecha devolución

    tk.Label(container, text="Fecha devolución", bg=BG, fg=TXT).pack()

    fecha = DateEntry(
        container,
        width=18,
        date_pattern="yyyy-mm-dd"
    )

    fecha.pack(pady=5)
  
    # Guardar

    def guardar():
        if combo.get() == "":
            messagebox.showerror("Error", "Seleccione un libro.")
            return
        if cedula.get() == "":
            messagebox.showerror("Error", "Ingrese la cédula.")
            return
        if cliente.get() == "":
            messagebox.showerror("Error", "Ingrese el nombre del cliente.")
            return
        id_libro = int(combo.get().split(" - ")[0])


        fecha_renta = datetime.date.today()
        fecha_dev = fecha.get_date()
        try:
            cursor.execute("""
                INSERT INTO rentas
                (
                    id_libro,
                    cedula,
                    cliente,
                    cantidad,
                    fecha_renta,
                    fecha_devolucion
                )
                VALUES
                (%s,%s,%s,%s,%s,%s)""",
            (
                id_libro,
                cedula.get(),
                cliente.get(),
                cantidad,
                fecha_renta,
                fecha_dev
            ))
           
            db.commit()
            messagebox.showinfo(
                "Éxito",
                "Renta registrada correctamente."
            )
            cursor.close()
            db.close()
            show_dvds(root, container, id_usuario)
        except mysql.connector.Error as err:
            messagebox.showerror(
                "Error",
                err
            )

    tk.Button(
        container,
        text="Guardar",
        bg=ROJO,
        fg=NEGRO,
        font=(FUENTE,11,"bold"),
        command=guardar
    ).pack(pady=10)

    tk.Button(
        container,
        text="Cancelar",
        command=lambda: show_dvds(root, container, id_usuario)
    ).pack()