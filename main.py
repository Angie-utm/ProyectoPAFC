import tkinter as tk
from tema import BG, aplicar_tema
from consultas.inicio import inicio_a

def main():
    root = tk.Tk()
    root.title("Sistema de Rentas de Libros")
    root.geometry("400x700")
    root.minsize(400, 700)
    root.maxsize(400, 700)
    root.configure(bg=BG)
    aplicar_tema(root)

  
    container = tk.Frame(root, bg=BG)
    container.pack(fill="both", expand=True)

    inicio_a(root, container)
    root.mainloop()

if __name__ == "__main__":
    main()
