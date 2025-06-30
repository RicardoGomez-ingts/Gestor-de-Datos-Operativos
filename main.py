import tkinter as tk
from tkinter import ttk
from revoke_segment import abrir_revoke_segment
from file_splitter import abrir_file_splitter

root = tk.Tk()
root.title("Gestor de Datos Operativos")
root.geometry("400x200")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")  # Prueba con: 'clam', 'alt', 'default', 'vista'

frame = ttk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Seleccione una opción", font=("Segoe UI", 14)).pack(pady=10)

ttk.Button(frame, text="Crear lista de Revoke Segment", width=35, command=lambda: abrir_revoke_segment(root)).pack(pady=5)
ttk.Button(frame, text="File Splitter (División de CSV)", width=35, command=lambda: abrir_file_splitter(root)).pack(pady=5)

root.mainloop()
