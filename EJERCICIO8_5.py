# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import datetime as dt


class Huesped:
    def __init__(self, nombre, apellidos, documento):
        self.nombre = nombre
        self.apellidos = apellidos
        self.documento = documento


class Habitacion:
    def __init__(self, numero, precio_dia):
        self.numero = numero
        self.precio_dia = precio_dia
        self.disponible = True
        self.huesped = None
        self.fecha_ingreso = None

    def ocupar(self, huesped, fecha_ingreso):
        self.huesped = huesped
        self.fecha_ingreso = fecha_ingreso
        self.disponible = False

    def liberar(self):
        self.huesped = None
        self.fecha_ingreso = None
        self.disponible = True


class VentanaHabitaciones(tk.Toplevel):
    """Ventana que muestra las habitaciones y permite elegir una para ocupar."""

    def __init__(self, master, habitaciones):
        super().__init__(master)
        self.title("Consultar habitaciones")
        self.habitaciones = habitaciones

        self.geometry("500x350")
        self.resizable(False, False)
        self.grab_set()

        self._crear_widgets()

    def _crear_widgets(self):
        columnas = ("numero", "precio", "estado")
        self.tree = ttk.Treeview(self, columns=columnas, show="headings")
        self.tree.heading("numero", text="Habitación")
        self.tree.heading("precio", text="Precio por día")
        self.tree.heading("estado", text="Estado")

        self.tree.column("numero", width=80, anchor="center")
        self.tree.column("precio", width=120, anchor="e")
        self.tree.column("estado", width=120, anchor="center")

        scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar_y.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Llenar la tabla
        self._refrescar_tabla()

        frame_abajo = tk.Frame(self, padx=10, pady=10)
        frame_abajo.pack(fill=tk.X, side=tk.BOTTOM)

        tk.Label(frame_abajo, text="Número de habitación a ocupar:").pack(side=tk.LEFT)
        self.entry_numero = tk.Entry(frame_abajo, width=5)
        self.entry_numero.pack(side=tk.LEFT, padx=5)

        btn_ocupar = tk.Button(frame_abajo, text="Ocupar habitación", command=self._ocuparseleccion)
        btn_ocupar.pack(side=tk.RIGHT)

    def _refrescar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for hab in self.habitaciones:
            estado = "Disponible" if hab.disponible else "No disponible"
            self.tree.insert(
                "", tk.END,
                values=(hab.numero, f"${hab.precio_dia:,.0f}", estado)
            )

    def _ocuparseleccion(self):
        texto = self.entry_numero.get().strip()
        if not texto.isdigit():
            messagebox.showerror("Error", "Debe ingresar un número de habitación válido.")
            return

        numero = int(texto)
        habitacion = self._buscar_habitacion(numero)

        if habitacion is None:
            messagebox.showerror("Error", "El número de habitación no existe.")
            return

        if not habitacion.disponible:
            messagebox.showerror("Error", "La habitación seleccionada ya está ocupada.")
            return

        # Abrir ventana de ingreso de huésped
        VentanaIngresoHuesped(self, habitacion, self._refrescar_tabla)

    def _buscar_habitacion(self, numero):
        for hab in self.habitaciones:
            if hab.numero == numero:
                return hab
        return None


class VentanaIngresoHuesped(tk.Toplevel):
    """Ventana para registrar el ingreso de un huésped a una habitación."""

    def __init__(self, master, habitacion, callback_actualizar):
        super().__init__(master)
        self.title(f"Ingreso huésped - Habitación {habitacion.numero}")
        self.habitacion = habitacion
        self.callback_actualizar = callback_actualizar

        self.geometry("400x320")
        self.resizable(False, False)
        self.grab_set()

        self._crear_widgets()

    def _crear_widgets(self):
        frame = tk.Frame(self, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text=f"Habitación {self.habitacion.numero} "
                             f"(${self.habitacion.precio_dia:,.0f} por día)").grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Fecha de ingreso
        tk.Label(frame, text="Fecha ingreso (AAAA-MM-DD):").grid(row=1, column=0, sticky="w")
        self.entry_fecha = tk.Entry(frame)
        self.entry_fecha.grid(row=1, column=1, sticky="ew")

        # Nombre
        tk.Label(frame, text="Nombre:").grid(row=2, column=0, sticky="w")
        self.entry_nombre = tk.Entry(frame)
        self.entry_nombre.grid(row=2, column=1, sticky="ew")

        # Apellidos
        tk.Label(frame, text="Apellidos:").grid(row=3, column=0, sticky="w")
        self.entry_apellidos = tk.Entry(frame)
        self.entry_apellidos.grid(row=3, column=1, sticky="ew")

        # Documento
        tk.Label(frame, text="Documento:").grid(row=4, column=0, sticky="w")
        self.entry_documento = tk.Entry(frame)
        self.entry_documento.grid(row=4, column=1, sticky="ew")

        frame_botones = tk.Frame(self)
        frame_botones.pack(fill=tk.X, side=tk.BOTTOM, pady=10)

        btn_guardar = tk.Button(frame_botones, text="Registrar ingreso", command=self._registrar_ingreso)
        btn_guardar.pack(side=tk.RIGHT, padx=5)

        btn_cerrar = tk.Button(frame_botones, text="Cerrar", command=self.destroy)
        btn_cerrar.pack(side=tk.RIGHT)

        frame.columnconfigure(1, weight=1)

    def _parse_fecha(self, texto):
        try:
            return dt.datetime.strptime(texto, "%Y-%m-%d").date()
        except ValueError:
            return None

    def _registrar_ingreso(self):
        fecha_txt = self.entry_fecha.get().strip()
        nombre = self.entry_nombre.get().strip()
        apellidos = self.entry_apellidos.get().strip()
        documento = self.entry_documento.get().strip()

        if not fecha_txt or not nombre or not apellidos or not documento:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        fecha_ingreso = self._parse_fecha(fecha_txt)
        if fecha_ingreso is None:
            messagebox.showerror("Error", "La fecha de ingreso no tiene el formato correcto (AAAA-MM-DD).")
            return

        huesped = Huesped(nombre, apellidos, documento)
        self.habitacion.ocupar(huesped, fecha_ingreso)

        messagebox.showinfo("Éxito", "Ingreso registrado correctamente.")
        self.callback_actualizar()   # Actualizar tabla de habitaciones
        self.destroy()


class VentanaSalidaSeleccion(tk.Toplevel):
    """Ventana que solicita el número de habitación para registrar salida."""

    def __init__(self, master, habitaciones):
        super().__init__(master)
        self.title("Salida de huéspedes - Seleccionar habitación")
        self.habitaciones = habitaciones

        self.geometry("350x150")
        self.resizable(False, False)
        self.grab_set()

        self._crear_widgets()

    def _crear_widgets(self):
        frame = tk.Frame(self, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Número de habitación a entregar:").pack()
        self.entry_numero = tk.Entry(frame, width=5)
        self.entry_numero.pack(pady=5)

        btn_continuar = tk.Button(frame, text="Continuar", command=self._continuar)
        btn_continuar.pack(pady=5)

    def _buscar_habitacion(self, numero):
        for hab in self.habitaciones:
            if hab.numero == numero:
                return hab
        return None

    def _continuar(self):
        texto = self.entry_numero.get().strip()
        if not texto.isdigit():
            messagebox.showerror("Error", "Debe ingresar un número de habitación válido.")
            return

        numero = int(texto)
        habitacion = self._buscar_habitacion(numero)

        if habitacion is None:
            messagebox.showerror("Error", "El número de habitación no existe.")
            return

        if habitacion.disponible:
            messagebox.showerror("Error", "La habitación no está ocupada.")
            return

        # Abrir ventana de registro de salida
        VentanaRegistrarSalida(self, habitacion)
        self.destroy()


class VentanaRegistrarSalida(tk.Toplevel):
    """Ventana donde se registra la fecha de salida, días y total a pagar."""

    def __init__(self, master, habitacion):
        super().__init__(master)
        self.title(f"Registrar salida - Habitación {habitacion.numero}")
        self.habitacion = habitacion
        self.fecha_salida = None

        self.geometry("430x300")
        self.resizable(False, False)
        self.grab_set()

        self._crear_widgets()

    def _crear_widgets(self):
        frame = tk.Frame(self, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        info = (
            f"Habitación {self.habitacion.numero} "
            f"(${self.habitacion.precio_dia:,.0f} por día)\n"
            f"Huésped: {self.habitacion.huesped.nombre} "
            f"{self.habitacion.huesped.apellidos}\n"
            f"Documento: {self.habitacion.huesped.documento}\n"
            f"Fecha ingreso: {self.habitacion.fecha_ingreso.isoformat()}"
        )
        tk.Label(frame, text=info, justify="left").grid(row=0, column=0, columnspan=2, sticky="w")

        tk.Label(frame, text="Fecha salida (AAAA-MM-DD):").grid(row=1, column=0, sticky="w", pady=(15, 0))
        self.entry_fecha_salida = tk.Entry(frame)
        self.entry_fecha_salida.grid(row=1, column=1, sticky="ew", pady=(15, 0))

        # Labels para mostrar resultados
        tk.Label(frame, text="Días de alojamiento:").grid(row=2, column=0, sticky="w", pady=(15, 0))
        self.lbl_dias = tk.Label(frame, text="-")
        self.lbl_dias.grid(row=2, column=1, sticky="w", pady=(15, 0))

        tk.Label(frame, text="Total a pagar:").grid(row=3, column=0, sticky="w")
        self.lbl_total = tk.Label(frame, text="-")
        self.lbl_total.grid(row=3, column=1, sticky="w")

        frame_botones = tk.Frame(self)
        frame_botones.pack(fill=tk.X, side=tk.BOTTOM, pady=10)

        self.btn_calcular = tk.Button(frame_botones, text="Calcular total", command=self._calcular_total)
        self.btn_calcular.pack(side=tk.RIGHT, padx=5)

        self.btn_registrar = tk.Button(frame_botones, text="Registrar salida", command=self._registrar_salida)
        self.btn_registrar.pack(side=tk.RIGHT)
        self.btn_registrar.config(state=tk.DISABLED)

        btn_cerrar = tk.Button(frame_botones, text="Cerrar", command=self.destroy)
        btn_cerrar.pack(side=tk.LEFT, padx=5)

        frame.columnconfigure(1, weight=1)

    def _parse_fecha(self, texto):
        try:
            return dt.datetime.strptime(texto, "%Y-%m-%d").date()
        except ValueError:
            return None

    def _calcular_total(self):
        fecha_txt = self.entry_fecha_salida.get().strip()
        if not fecha_txt:
            messagebox.showerror("Error", "Debe ingresar la fecha de salida.")
            return

        fecha_salida = self._parse_fecha(fecha_txt)
        if fecha_salida is None:
            messagebox.showerror("Error", "La fecha de salida no tiene el formato correcto (AAAA-MM-DD).")
            return

        if fecha_salida <= self.habitacion.fecha_ingreso:
            messagebox.showerror("Error", "La fecha de salida debe ser mayor a la fecha de ingreso.")
            return

        dias = (fecha_salida - self.habitacion.fecha_ingreso).days
        total = dias * self.habitacion.precio_dia

        self.fecha_salida = fecha_salida
        self.lbl_dias.config(text=str(dias))
        self.lbl_total.config(text=f"${total:,.0f}")

        # Si la fecha es correcta y ya se calculó, habilitar botón de registrar salida
        self.btn_registrar.config(state=tk.NORMAL)

    def _registrar_salida(self):
        if self.fecha_salida is None:
            messagebox.showerror("Error", "Primero debe calcular el total.")
            return

        self.habitacion.liberar()
        messagebox.showinfo("Éxito", "Salida registrada. La habitación ha quedado disponible.")
        self.destroy()


class HotelApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Hotel")
        self.geometry("600x400")
        self.resizable(True, True)

        self.habitaciones = []
        self._crear_habitaciones()
        self._crear_menu()
        self._crear_contenido_principal()

    def _crear_habitaciones(self):
        # Habitaciones 1 a 5 -> $120 000
        for i in range(1, 6):
            self.habitaciones.append(Habitacion(i, 120000))
        # Habitaciones 6 a 10 -> $160 000
        for i in range(6, 11):
            self.habitaciones.append(Habitacion(i, 160000))

    def _crear_menu(self):
        menubar = tk.Menu(self)

        menu_opciones = tk.Menu(menubar, tearoff=0)
        menu_opciones.add_command(label="Consultar habitaciones", command=self._abrir_consulta_habitaciones)
        menu_opciones.add_command(label="Salida de huéspedes", command=self._abrir_salida_huespedes)

        menubar.add_cascade(label="Opciones", menu=menu_opciones)
        self.config(menu=menubar)

    def _crear_contenido_principal(self):
        lbl = tk.Label(
            self,
            text=(
                "Bienvenido al sistema de gestión del hotel.\n\n"
                "Use el menú 'Opciones' para:\n"
                " - Consultar habitaciones e ingresar huéspedes\n"
                " - Registrar la salida de huéspedes"
            ),
            justify="center"
        )
        lbl.pack(expand=True)

    def _abrir_consulta_habitaciones(self):
        VentanaHabitaciones(self, self.habitaciones)

    def _abrir_salida_huespedes(self):
        VentanaSalidaSeleccion(self, self.habitaciones)


if __name__ == "__main__":
    app = HotelApp()
    app.mainloop()
