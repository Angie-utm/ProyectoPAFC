import tkinter as tk
from tkinter import messagebox
import mysql.connector
from bd import iniciar_bd
import os
import cv2
import numpy as np
from tema import *

def reconocimiento_facial():
    if not os.path.exists("rostros_guardados"):
        os.makedirs("rostros_guardados")
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    video_capture = cv2.VideoCapture(0)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_count = 0
    rostro = False
    def detect_bounding_box(vid):
        gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
        return faces
    def train_recognizer():
        faces = []
        labels = []
        label = 0
        for i in range(1, 6):
            image_path = f'rostros_guardados/rostro_{i}.jpg'
            if os.path.exists(image_path):
                img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                cv2.imwrite(f'rostros_guardados/rostro_10.jpg', img)
                faces.append(img)
                labels.append(label)
        recognizer.train(faces, np.array(labels))
        recognizer.save('modelo_reconocimiento.yml')
    train_recognizer()
    while True:
        result, video_frame = video_capture.read()
        if not result:
            break
        faces = detect_bounding_box(video_frame)
        for (x, y, w, h) in faces:
            gray_face = cv2.cvtColor(video_frame[y:y + h, x:x + w], cv2.COLOR_BGR2GRAY)
            label, confidence = recognizer.predict(gray_face)
            if confidence < 60:
                cv2.putText(video_frame, f'Persona {label}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                face_count = 1
            else:
                cv2.putText(video_frame, "Desconocido", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        cv2.imshow("Rostro", video_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        if face_count == 1:
            rostro = True
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return rostro

def iniciar_sesion_a(root, container):
    from consultas.regreso import regresar
    from consultas.lista_libros import show_dvds
    for w in container.winfo_children():
        w.destroy()
    regresar(root, container)

    tk.Label(container, text="Iniciar Sesión", bg=BG, fg=ROJO, font=(FUENTE, 20, "bold")).pack(pady=(10, 10))
    tk.Frame(container, height=10, bg=BG).pack()

    tk.Label(container, text="Usuario", bg=BG, fg=TXT, font=(FUENTE, 11)).pack()
    username = tk.Entry(container, width=30, bg=FONDO_CAMPO, fg=NEGRO)
    username.pack(pady=(2, 12))
    username.focus_set()

    tk.Label(container, text="Contraseña", bg=BG, fg=TXT, font=(FUENTE, 11)).pack()
    contraseña = tk.Entry(container, width=30, show="*", bg=FONDO_CAMPO, fg=NEGRO)
    contraseña.pack(pady=(2, 15))

    def rostro_click():
        username_val = username.get()

        try:
            db = iniciar_bd()
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuario WHERE  username = %s", (username_val,))
            user = cursor.fetchone()
            db.close()

            if user:
                ruta_rostros = 'rostros_guardados'
                for i in range(1, 6):
                    imagen_blob = user[f'rostro_{i}']
                    ruta_archivo = os.path.join(ruta_rostros, f"rostro_{i}.jpg")
                    with open(ruta_archivo, "wb") as archivo:
                        archivo.write(imagen_blob)

                rostro = reconocimiento_facial()
                for i in range(1, 6):
                    ruta_archivo = os.path.join(ruta_rostros, f"rostro_{i}.jpg")
                    if os.path.exists(ruta_archivo):
                        os.remove(ruta_archivo)
                if rostro:
                    messagebox.showinfo("Bienvenido", f"¡Bienvenido, {user['nombre']}!")
                    id_usuario = user['id_usuario']
                    show_dvds(root, container, id_usuario)
                else:
                    messagebox.showerror("Error", "No se reconoció el rostro.")
            else:
                messagebox.showerror("Error", "Credenciales incorrectas.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error en la conexión", f"Error en la conexión: {err}")

    def login_click():
        username_val = username.get()
        contraseña_val = contraseña.get()

        try:
            db = iniciar_bd()
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuario WHERE (username = %s) AND contraseña = %s", (username_val, contraseña_val))
            user = cursor.fetchone()
            db.close()

            if user:
                messagebox.showinfo("Bienvenido", f"¡Bienvenido, {user['nombre']}!")
                id_usuario = user['id_usuario']
                show_dvds(root, container, id_usuario)
            else:
                messagebox.showerror("Error", "Credenciales incorrectas.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error en la conexión", f"Error en la conexión: {err}")

    tk.Button(
        container,
        text="Iniciar Sesión",
        width=22,
        bg=ROJO,
        fg=NEGRO,
        activebackground=ROJO,
        activeforeground=NEGRO,
        font=(FUENTE, 11, "bold"),
        command=login_click,
    ).pack(pady=5)

    tk.Button(
        container,
        text="Iniciar Con Reconocimiento Facial",
        width=28,
        bg=ROJO,
        fg=NEGRO,
        activebackground=ROJO,
        activeforeground=NEGRO,
        font=(FUENTE, 10, "bold"),
        command=rostro_click,
    ).pack(pady=5)

    tk.Label(
        container,
        text="Si inicia sesión con reconocimiento facial necesita agregar su usuario...",
        bg=BG,
        fg=ROJO,
        font=(FUENTE, 9),
    ).pack(pady=10)
