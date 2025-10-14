import tkinter as tk
from tkinter import ttk, messagebox
import math

# --------------------- CLASES DE FIGURAS ---------------------

class Figura:
    def volumen(self):
        pass
    def superficie(self):
        pass

class Cilindro(Figura):
    def __init__(self, radio, altura):
        self.radio = radio
        self.altura = altura
    def volumen(self):
        return math.pi * self.radio**2 * self.altura
    def superficie(self):
        return 2 * math.pi * self.radio * (self.radio + self.altura)

class Esfera(Figura):
    def __init__(self, radio):
        self.radio = radio
    def volumen(self):
        return (4/3) * math.pi * self.radio**3
    def superficie(self):
        return 4 * math.pi * self.radio**2

class Piramide(Figura):
    def __init__(self, base, altura, apotema):
        self.base = base
        self.altura = altura
        self.apotema = apotema
    def volumen(self):
        return (1/3) * (self.base**2) * self.altura
    def superficie(self):
        return (self.base**2) + 2 * (self.base * self.apotema / 2)

class Cubo(Figura):
    def __init__(self, lado):
        self.lado = lado
    def volumen(self):
        return self.lado**3
    def superficie(self):
        return 6 * self.lado**2

class Prisma(Figura):
    def __init__(self, base, altura, profundidad):
        self.base = base
        self.altura = altura
        self.profundidad = profundidad
    def volumen(self):
        return self.base * self.altura * self.profundidad
    def superficie(self):
        return 2 * (self.base * self.altura + self.base * self.profundidad + self.altura * self.profundidad)

# --------------------- INTERFAZ GRÁFICA ---------------------

ventana = tk.Tk()
ventana.title("Cálculo de Volumen y Superficie de Figuras Geométricas")
ventana.geometry("500x550")
ventana.resizable(False, False)

# Selector de figura
tk.Label(ventana, text="Seleccione una figura geométrica:", font=("Arial", 12)).pack(pady=5)
figura_var = tk.StringVar()
combo_figura = ttk.Combobox(ventana, textvariable=figura_var, state="readonly",
                            values=["Cilindro", "Esfera", "Pirámide", "Cubo", "Prisma"])
combo_figura.pack(pady=5)

# Frame de entradas dinámicas
frame_entradas = tk.Frame(ventana)
frame_entradas.pack(pady=10)

entradas = {}

def mostrar_campos(*args):
    # Limpiar frame
    for widget in frame_entradas.winfo_children():
        widget.destroy()
    entradas.clear()
    figura = figura_var.get()

    campos = []
    if figura == "Cilindro":
        campos = ["Radio", "Altura"]
    elif figura == "Esfera":
        campos = ["Radio"]
    elif figura == "Pirámide":
        campos = ["Base", "Altura", "Apotema"]
    elif figura == "Cubo":
        campos = ["Lado"]
    elif figura == "Prisma":
        campos = ["Base", "Altura", "Profundidad"]

    # Crear campos de entrada
    for campo in campos:
        frame = tk.Frame(frame_entradas)
        frame.pack(pady=3)
        tk.Label(frame, text=f"{campo} (cm):").pack(side="left")
        entrada = tk.Entry(frame)
        entrada.pack(side="left", padx=5)
        entradas[campo.lower()] = entrada

combo_figura.bind("<<ComboboxSelected>>", mostrar_campos)

# Etiqueta resultado
etiqueta_resultado = tk.Label(ventana, text="", font=("Arial", 11), justify="left")
etiqueta_resultado.pack(pady=10)

# --------------------- FUNCIONES ---------------------

def calcular():
    figura = figura_var.get()
    if not figura:
        messagebox.showerror("Error", "Debe seleccionar una figura.")
        return

    # Validar entradas
    valores = {}
    for nombre, entrada in entradas.items():
        valor = entrada.get().strip()
        if valor == "":
            messagebox.showerror("Error", f"Debe ingresar el valor de {nombre}.")
            return
        try:
            num = float(valor)
            if num <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", f"El valor de {nombre} debe ser un número positivo.")
            return
        valores[nombre] = num

    # Crear figura y calcular
    if figura == "Cilindro":
        obj = Cilindro(valores["radio"], valores["altura"])
    elif figura == "Esfera":
        obj = Esfera(valores["radio"])
    elif figura == "Pirámide":
        obj = Piramide(valores["base"], valores["altura"], valores["apotema"])
    elif figura == "Cubo":
        obj = Cubo(valores["lado"])
    elif figura == "Prisma":
        obj = Prisma(valores["base"], valores["altura"], valores["profundidad"])

    vol = obj.volumen()
    sup = obj.superficie()

    etiqueta_resultado.config(
        text=f"Volumen: {vol:.2f} cm³\nSuperficie: {sup:.2f} cm²"
    )

def limpiar():
    for entrada in entradas.values():
        entrada.delete(0, tk.END)
    etiqueta_resultado.config(text="")
    figura_var.set("")

def salir():
    ventana.destroy()

# --------------------- BOTONES ---------------------

frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=15)

tk.Button(frame_botones, text="Calcular", command=calcular, bg="#4CAF50", fg="white", width=12).pack(side="left", padx=5)
tk.Button(frame_botones, text="Limpiar", command=limpiar, bg="#E53935", fg="white", width=12).pack(side="left", padx=5)
tk.Button(frame_botones, text="Salir", command=salir, bg="#757575", fg="white", width=12).pack(side="left", padx=5)

ventana.mainloop()
