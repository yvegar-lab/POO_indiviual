import tkinter as tk
from tkinter import messagebox
import statistics

def calcular():
    notas = []
    for i in range(5):
        valor = entradas[i].get().strip()
        if valor == "":
            messagebox.showerror("Error", f"Debe ingresar la nota {i+1}.")
            return
        try:
            nota = float(valor)
        except ValueError:
            messagebox.showerror("Error", f"La nota {i+1} no es un número válido.")
            return
        if nota < 0 or nota > 5:
            messagebox.showerror("Error", f"La nota {i+1} debe estar entre 0 y 5.")
            return
        notas.append(nota)

    promedio = sum(notas) / len(notas)
    desviacion = statistics.stdev(notas)
    mayor = max(notas)
    menor = min(notas)

    etiqueta_resultado.config(
        text=(
            f"Promedio: {promedio:.2f}\n"
            f"Desviación estándar: {desviacion:.2f}\n"
            f"Nota más alta: {mayor:.2f}\n"
            f"Nota más baja: {menor:.2f}"
        )
    )

def limpiar():
    for entrada in entradas:
        entrada.delete(0, tk.END)
    etiqueta_resultado.config(text="")

def salir():
    ventana.destroy()

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Cálculo de Notas del Estudiante")
ventana.geometry("420x440")
ventana.resizable(False, False)

tk.Label(ventana, text="Ingrese las 5 notas del estudiante:", font=("Arial", 12)).pack(pady=10)

entradas = []
for i in range(5):
    frame = tk.Frame(ventana)
    frame.pack(pady=3)
    tk.Label(frame, text=f"Nota {i+1}:").pack(side="left")
    entrada = tk.Entry(frame)
    entrada.pack(side="left", padx=5)
    entradas.append(entrada)

# Frame para los botones
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=20)

# Botón Calcular (verde)
tk.Button(frame_botones, text="Calcular", command=calcular, bg="#4CAF50", fg="white", width=12).pack(side="left", padx=5)

# Botón Limpiar (rojo)
tk.Button(frame_botones, text="Limpiar", command=limpiar, bg="#E53935", fg="white", width=12).pack(side="left", padx=5)

# Botón Salir (gris)
tk.Button(frame_botones, text="Salir", command=salir, bg="#757575", fg="white", width=12).pack(side="left", padx=5)

# Etiqueta de resultados
etiqueta_resultado = tk.Label(ventana, text="", font=("Arial", 11), justify="left")
etiqueta_resultado.pack(pady=10)

ventana.mainloop()
