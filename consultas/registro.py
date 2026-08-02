import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import mysql.connector
from bd import iniciar_bd
import os
import cv2
import time
import datetime
from tema import *
from consultas.regreso import regresar

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

def campo(parent, texto):
    tk.Label(parent, text=texto, bg=BG, fg=TXT, font=(FUENTE, 11)).pack()
    entry = tk.Entry(parent, width=30, bg=FONDO_CAMPO, fg=NEGRO)
    entry.pack(pady=(2, 10))
    return entry

def registro_usuario(root, container):
    from consultas.inicio import inicio_a
    for w in container.winfo_children():
        w.destroy()
    regresar(root, container)

    _, frame = crear_scrollable(container)

    tk.Label(frame, text="Registro de Usuario", bg=BG, fg=ROJO, font=(FUENTE, 20, "bold")).pack(pady=(5, 15))

    nombre = campo(frame, "Nombre")
    apellido = campo(frame, "Apellido")
    usuario = campo(frame, "Usuario")
    tk.Label(frame, text="Contraseña", bg=BG, fg=TXT, font=(FUENTE, 11)).pack()
    contraseña = tk.Entry(frame, width=30, show="*", bg=FONDO_CAMPO, fg=NEGRO)
    contraseña.pack(pady=(2, 10))
    nombre.focus_set()


    def registrar_click():
        if not nombre.get() or not apellido.get() or not usuario.get() or not contraseña.get():
            messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return

        face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        video_capture = cv2.VideoCapture(0)

        if not os.path.exists("rostros_guardados"):
            os.makedirs("rostros_guardados")

        def detect_bounding_box(vid):
            gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
            return faces

        face_count = 0
        start_time = time.time()
        rostros_blob = []
        while True:
            result, video_frame = video_capture.read()
            if not result:
                break

            faces = detect_bounding_box(video_frame)

            if len(faces) > 0 and face_count < 5 and (time.time() - start_time) >= 0.5:
                for (x, y, w, h) in faces:
                    rostro = video_frame[y:y + h, x:x + w]
                    success, encoded_image = cv2.imencode(".jpg", rostro)
                    if success:
                        rostro_blob = encoded_image.tobytes()
                        rostros_blob.append(rostro_blob)
                        face_count += 1
                        start_time = time.time()

            cv2.imshow("Captura de Rostros", video_frame)
            if cv2.waitKey(1) & 0xFF == ord("q") or face_count >= 5:
                break

        video_capture.release()
        cv2.destroyAllWindows()

        if len(rostros_blob) < 5:
            messagebox.showerror("Error", "No se capturaron suficientes rostros. Se requieren 5 rostros.")
            return
        try:
            db = iniciar_bd()
            cursor = db.cursor()

            query = """
                INSERT INTO usuario (nombre, apellido, contraseña, rostro_1, rostro_2, rostro_3, rostro_4, rostro_5, username)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                nombre.get(), 
                apellido.get(), 
                contraseña.get(), 
                rostros_blob[0], 
                rostros_blob[1], 
                rostros_blob[2], 
                rostros_blob[3],
                rostros_blob[4], 
                usuario.get()
            ))
            db.commit()
            cursor.close()
            db.close()

            rostros_blob.clear()

            messagebox.showinfo("Éxito", "Usuario registrado con éxito.")
            inicio_a(root, container)
        except mysql.connector.Error as err:
            messagebox.showerror("Error en la conexión", f"Error en la conexión: {err}")

    tk.Button(
        frame,
        text="Registrarse",
        width=20,
        bg=ROJO,
        fg=NEGRO,
        activebackground=ROJO,
        activeforeground=NEGRO,
        font=(FUENTE, 12, "bold"),
        command=registrar_click,
    ).pack(pady=(10, 5))

    tk.Frame(frame, height=20, bg=BG).pack()
