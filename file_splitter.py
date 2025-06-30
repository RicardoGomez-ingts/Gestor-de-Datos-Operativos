import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import csv
import os

def abrir_file_splitter(parent):
    ventana = tk.Toplevel(parent)
    ventana.title("División de Archivos CSV")
    ventana.geometry("500x350")
    ventana.resizable(False, False)

    file_path = tk.StringVar()
    output_path = tk.StringVar()
    line_limit = tk.StringVar()
    include_headers = tk.BooleanVar()

    def seleccionar_archivo():
        ruta = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if ruta:
            file_path.set(ruta)

    def seleccionar_carpeta():
        carpeta = filedialog.askdirectory()
        if carpeta:
            output_path.set(carpeta)

    def dividir_archivo():
        if not file_path.get().strip():
            messagebox.showwarning("Falta información", "Por favor selecciona un archivo CSV.")
            return
        if not line_limit.get().strip().isdigit():
            messagebox.showwarning("Número inválido", "Por favor ingresa un número válido de líneas por archivo.")
            return
        if not output_path.get().strip():
            messagebox.showwarning("Falta información", "Por favor selecciona una carpeta de destino.")
            return

        try:
            line_count = int(line_limit.get())
            with open(file_path.get(), newline='', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                headers = next(reader) if include_headers.get() else None

                file_counter = 1
                current_lines = []
                base_name = os.path.splitext(os.path.basename(file_path.get()))[0]

                for i, row in enumerate(reader, start=1):
                    current_lines.append(row)
                    if len(current_lines) == line_count:
                        output_file = os.path.join(output_path.get(), f"{base_name}_part{file_counter}.csv")
                        with open(output_file, "w", newline='', encoding='utf-8') as outfile:
                            writer = csv.writer(outfile)
                            if headers:
                                writer.writerow(headers)
                            writer.writerows(current_lines)
                        current_lines = []
                        file_counter += 1

                if current_lines:
                    output_file = os.path.join(output_path.get(), f"{base_name}_part{file_counter}.csv")
                    with open(output_file, "w", newline='', encoding='utf-8') as outfile:
                        writer = csv.writer(outfile)
                        if headers:
                            writer.writerow(headers)
                        writer.writerows(current_lines)

            messagebox.showinfo("Éxito", f"Archivo dividido correctamente en {file_counter} partes.")
            ventana.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al dividir el archivo:\n{str(e)}")

    ttk.Label(ventana, text="Archivo CSV a dividir:").pack(anchor="w", padx=10, pady=(10, 0))
    ttk.Entry(ventana, textvariable=file_path, width=50).pack(padx=10)
    ttk.Button(ventana, text="Seleccionar archivo", command=seleccionar_archivo).pack(padx=10, pady=2)

    ttk.Label(ventana, text="Líneas por archivo:").pack(anchor="w", padx=10, pady=(10, 0))
    ttk.Entry(ventana, textvariable=line_limit, width=20).pack(padx=10)

    ttk.Checkbutton(ventana, text="Incluir encabezados", variable=include_headers).pack(padx=10, pady=(5, 10))

    ttk.Label(ventana, text="Carpeta de destino:").pack(anchor="w", padx=10, pady=(10, 0))
    ttk.Entry(ventana, textvariable=output_path, width=50).pack(padx=10)
    ttk.Button(ventana, text="Seleccionar carpeta", command=seleccionar_carpeta).pack(padx=10, pady=2)

    ttk.Button(ventana, text="Dividir archivo", command=dividir_archivo).pack(pady=20)
