import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
import datetime
import os

def abrir_revoke_segment(parent):
    ventana = tk.Toplevel(parent)
    ventana.title("Crear lista de Revoke Segment")
    ventana.geometry("500x300")
    ventana.resizable(False, False)

    segment_name = tk.StringVar()
    file_path = tk.StringVar()
    output_path = tk.StringVar()

    def seleccionar_archivo():
        ruta = filedialog.askopenfilename(filetypes=[("CSV/TXT files", "*.csv *.txt")])
        if ruta:
            file_path.set(ruta)

    def seleccionar_carpeta():
        carpeta = filedialog.askdirectory()
        if carpeta:
            output_path.set(carpeta)

    def crear_archivo():
        if not segment_name.get().strip():
            messagebox.showwarning("Falta información", "Por favor ingrese el nombre del segmento.")
            return
        if not file_path.get().strip():
            messagebox.showwarning("Falta información", "Por favor seleccione un archivo de entrada.")
            return
        if not output_path.get().strip():
            messagebox.showwarning("Falta información", "Por favor seleccione la carpeta de destino.")
            return

        try:
            if file_path.get().lower().endswith(".csv"):
                df = pd.read_csv(file_path.get(), header=None, names=["ConsultantID"])
            else:
                with open(file_path.get(), "r") as f:
                    lines = f.read().splitlines()
                df = pd.DataFrame(lines, columns=["ConsultantID"])

            df["SegmentID"] = segment_name.get().strip()
            df["RevokeDate"] = datetime.date.today().isoformat()
            df["Comments"] = ""

            nombre_archivo = f"revoke_segment_{segment_name.get().strip().replace(' ', '_')}.csv"
            ruta_final = os.path.join(output_path.get(), nombre_archivo)
            df.to_csv(ruta_final, index=False)

            messagebox.showinfo("Éxito", f"Archivo generado correctamente:\n{ruta_final}")
            ventana.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al procesar el archivo:\n{str(e)}")

    ttk.Label(ventana, text="Nombre del segmento:").pack(anchor="w", padx=10, pady=(10, 0))
    ttk.Entry(ventana, textvariable=segment_name, width=50).pack(padx=10)

    ttk.Label(ventana, text="Archivo con lista de consultoras:").pack(anchor="w", padx=10, pady=(10, 0))
    ttk.Entry(ventana, textvariable=file_path, width=50).pack(padx=10)
    ttk.Button(ventana, text="Seleccionar archivo", command=seleccionar_archivo).pack(padx=10, pady=2)

    ttk.Label(ventana, text="Carpeta de destino:").pack(anchor="w", padx=10, pady=(10, 0))
    ttk.Entry(ventana, textvariable=output_path, width=50).pack(padx=10)
    ttk.Button(ventana, text="Seleccionar carpeta", command=seleccionar_carpeta).pack(padx=10, pady=2)

    ttk.Button(ventana, text="Crear archivo", command=crear_archivo).pack(pady=20)

