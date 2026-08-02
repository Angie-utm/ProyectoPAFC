import tkinter as tk
from bd import iniciar_bd
from tema import *

def crear_scrollable(parent):
    canvas = tk.Canvas(parent, bg=BG, highlightthickness=0)
    scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    frame = tk.Frame(canvas, bg=BG)

    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def _wheel(event):
        try:
            canvas.yview_scroll(int(-event.delta / 120), "units")
        except tk.TclError:
            pass

    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _wheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(1, width=e.width))

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    return canvas, frame

def barra_navegacion(parent, root, container, id_usuario, seleccion):
    from consultas.configuracion import conf

    def estilo_activo():
        return {"bg": AMBER, "fg": NEGRO}

    def estilo_inactivo():
        return {"bg": BG_SEC, "fg": TXT}

    nav = tk.Frame(parent, bg=BG_SEC, height=56)
    nav.pack(side="bottom", fill="x")

    btn_renta = tk.Button(
        nav,
        text="Renta",
        relief="flat",
        activebackground=AMBER,
        activeforeground=NEGRO,
        font=(FUENTE, 11, "bold"),
        command=lambda: lista_rentas(root, container, id_usuario),
    )
    btn_usuario = tk.Button(
        nav,
        text="Usuario",
        relief="flat",
        activebackground=AMBER,
        activeforeground=NEGRO,
        font=(FUENTE, 11, "bold"),
        command=lambda: conf(root, container, id_usuario),
    )

    if seleccion == 0:
        btn_renta.configure(**estilo_activo())
        btn_usuario.configure(**estilo_inactivo())
    else:
        btn_renta.configure(**estilo_inactivo())
        btn_usuario.configure(**estilo_activo())

    btn_renta.pack(side="left", expand=True, fill="both")
    btn_usuario.pack(side="left", expand=True, fill="both")

def lista_rentas(root, container, id_usuario):
    from consultas.agregar_libro import agregar_libro
    from consultas.agregar_renta import agregar_renta
    for w in container.winfo_children():
        w.destroy()
    frame_b= tk.Frame(container, bg=BG)
    frame_b.pack(pady=10)
    b_libro=tk.Button(frame_b, 
              text="Agregar Libro", 
              bg=ROJO, fg=NEGRO, 
              activebackground=ROJO, 
              activeforeground=NEGRO,
              command=lambda: agregar_libro(root, container, id_usuario),
              font=(FUENTE, 10, "bold"))
    
    b_renta=tk.Button(frame_b, 
              text="Agregar Renta", 
              bg=ROJO, fg=NEGRO, 
              activebackground=ROJO, 
              activeforeground=NEGRO,
              command=lambda: agregar_renta(root, container, id_usuario),
              font=(FUENTE, 10, "bold"))

    
    b_libro.grid(row=0, column=0, padx=5)
    b_renta.grid(row=0, column=1, padx=5)
    tk.Label(container, text="Rentas:", bg=BG, fg=ROJO, font=(FUENTE, 16, "bold")).pack(pady=10)

    barra_navegacion(container, root, container, id_usuario, 0)

    _, frame = crear_scrollable(container)

    db = iniciar_bd()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
                    SELECT
                        r.id_renta,
                        l.titulo,
                        r.cliente,
                        r.cedula,
                        r.cantidad,
                        r.fecha_renta,
                        r.fecha_devolucion
                    FROM rentas r
                    INNER JOIN libros l
                    ON r.id_libro = l.id_libro
                    ORDER BY r.fecha_renta DESC
                    """)
    rentas = cursor.fetchall()
    db.close()


    for renta in rentas:
        card = tk.Frame(frame, bg=CARD, highlightthickness=0)
        card.pack(fill="x", padx=10, pady=8)
        tk.Label(card, text="Libro:", bg=CARD, fg=TXT, font=(FUENTE, 10, "bold")).pack(anchor="w")
        tk.Label(card, text=renta["titulo"], bg=CARD, fg=TXT, font=(FUENTE, 12, "bold")).pack(anchor="w", pady=(5, 2))
        tk.Label(card, text="Cliente:", bg=CARD, fg=TXT, font=(FUENTE, 10, "bold")).pack(anchor="w")
        tk.Label(card, text=renta["cliente"], bg=CARD, fg=TXT).pack(anchor="w")
        tk.Label(card, text="Fecha de renta:", bg=CARD, fg=TXT, font=(FUENTE, 10, "bold")).pack(anchor="w")
        tk.Label(card, text=renta["fecha_renta"], bg=CARD, fg=TXT, wraplength=320, justify="left").pack(anchor="w")
        tk.Label(card, text="Fecha de devolución:", bg=CARD, fg=TXT, font=(FUENTE, 10, "bold")).pack(anchor="w")
        tk.Label(card, text=renta["fecha_devolucion"], bg=CARD, fg=TXT, wraplength=320, justify="left").pack(anchor="w")

        fila = tk.Frame(card, bg=CARD)
        fila.pack(anchor="w", pady=(0, 5))

    tk.Frame(frame, height=20, bg=BG).pack()
