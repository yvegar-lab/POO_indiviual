# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os


class Empleado:
    """Clase de dominio que representa un empleado."""

    def __init__(self, nombre, apellidos, cargo, genero,
                 salario_dia, dias_trabajados,
                 otros_ingresos, pagos_salud, aporte_pension):
        self.nombre = nombre
        self.apellidos = apellidos
        self.cargo = cargo            # Directivo, Estratégico, Operativo
        self.genero = genero          # Masculino, Femenino
        self.salario_dia = salario_dia
        self.dias_trabajados = dias_trabajados
        self.otros_ingresos = otros_ingresos
        self.pagos_salud = pagos_salud
        self.aporte_pension = aporte_pension

    def calcular_salario_mensual(self):
        """
        Salario mensual = (días trabajados * sueldo por día)
                          + otros ingresos
                          - pagos por salud
                          - aporte pensiones
        """
        return (self.dias_trabajados * self.salario_dia) \
            + self.otros_ingresos \
            - self.pagos_salud \
            - self.aporte_pension


class AgregarEmpleadoWindow(tk.Toplevel):
    """Ventana para agregar un empleado."""

    def __init__(self, master, lista_empleados):
        super().__init__(master)
        self.title("Agregar empleado")
        self.lista_empleados = lista_empleados

        self.geometry("450x430")
        self.resizable(False, False)
        self.grab_set()  # Hace modal la ventana

        self._crear_widgets()

    def _crear_widgets(self):
        frame = tk.Frame(self, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Nombre
        tk.Label(frame, text="Nombre:").grid(row=0, column=0, sticky="w")
        self.entry_nombre = tk.Entry(frame)
        self.entry_nombre.grid(row=0, column=1, sticky="ew")

        # Apellidos
        tk.Label(frame, text="Apellidos:").grid(row=1, column=0, sticky="w")
        self.entry_apellidos = tk.Entry(frame)
        self.entry_apellidos.grid(row=1, column=1, sticky="ew")

        # Cargo (JList -> Listbox)
        tk.Label(frame, text="Cargo:").grid(row=2, column=0, sticky="nw")
        self.list_cargo = tk.Listbox(frame, height=3, exportselection=False)
        for c in ["Directivo", "Estratégico", "Operativo"]:
            self.list_cargo.insert(tk.END, c)
        self.list_cargo.grid(row=2, column=1, sticky="ew")

        # Género (CheckBox simulando exclusividad)
        tk.Label(frame, text="Género:").grid(row=3, column=0, sticky="w")
        genero_frame = tk.Frame(frame)
        genero_frame.grid(row=3, column=1, sticky="w")

        self.var_masculino = tk.IntVar(value=0)
        self.var_femenino = tk.IntVar(value=0)

        self.chk_masculino = tk.Checkbutton(
            genero_frame, text="Masculino",
            variable=self.var_masculino,
            command=self._seleccion_genero_masculino
        )
        self.chk_masculino.pack(side=tk.LEFT)

        self.chk_femenino = tk.Checkbutton(
            genero_frame, text="Femenino",
            variable=self.var_femenino,
            command=self._seleccion_genero_femenino
        )
        self.chk_femenino.pack(side=tk.LEFT)

        # Salario por día
        tk.Label(frame, text="Salario por día:").grid(row=4, column=0, sticky="w")
        self.entry_salario_dia = tk.Entry(frame)
        self.entry_salario_dia.grid(row=4, column=1, sticky="ew")

        # Días trabajados (JSpinner -> Spinbox)
        tk.Label(frame, text="Días trabajados (1-31):").grid(row=5, column=0, sticky="w")
        self.var_dias = tk.IntVar(value=1)
        self.spin_dias = tk.Spinbox(
            frame, from_=1, to=31, textvariable=self.var_dias, width=5
        )
        self.spin_dias.grid(row=5, column=1, sticky="w")

        # Otros ingresos
        tk.Label(frame, text="Otros ingresos:").grid(row=6, column=0, sticky="w")
        self.entry_otros_ingresos = tk.Entry(frame)
        self.entry_otros_ingresos.grid(row=6, column=1, sticky="ew")

        # Pagos salud
        tk.Label(frame, text="Pagos por salud:").grid(row=7, column=0, sticky="w")
        self.entry_pagos_salud = tk.Entry(frame)
        self.entry_pagos_salud.grid(row=7, column=1, sticky="ew")

        # Aporte pensiones
        tk.Label(frame, text="Aporte pensiones:").grid(row=8, column=0, sticky="w")
        self.entry_aporte_pension = tk.Entry(frame)
        self.entry_aporte_pension.grid(row=8, column=1, sticky="ew")

        # Botones
        btn_frame = tk.Frame(self, pady=5)
        btn_frame.pack(fill=tk.X, side=tk.BOTTOM)

        btn_guardar = tk.Button(btn_frame, text="Guardar", command=self._guardar_empleado)
        btn_guardar.pack(side=tk.RIGHT, padx=5)

        btn_cerrar = tk.Button(btn_frame, text="Cerrar", command=self.destroy)
        btn_cerrar.pack(side=tk.RIGHT)

        # Configuración de columnas
        frame.columnconfigure(1, weight=1)

    def _seleccion_genero_masculino(self):
        if self.var_masculino.get() == 1:
            self.var_femenino.set(0)

    def _seleccion_genero_femenino(self):
        if self.var_femenino.get() == 1:
            self.var_masculino.set(0)

    def _parse_float(self, entry, nombre_campo, obligatorio=True):
        texto = entry.get().strip()
        if texto == "":
            if obligatorio:
                messagebox.showerror("Error", f'El campo "{nombre_campo}" es obligatorio.')
                return None
            else:
                return 0.0
        try:
            return float(texto)
        except ValueError:
            messagebox.showerror("Error", f'El campo "{nombre_campo}" debe ser un número.')
            return None

    def _guardar_empleado(self):
        nombre = self.entry_nombre.get().strip()
        apellidos = self.entry_apellidos.get().strip()

        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio.")
            return
        if not apellidos:
            messagebox.showerror("Error", "Los apellidos son obligatorios.")
            return

        # Cargo
        seleccion_cargo = self.list_cargo.curselection()
        if not seleccion_cargo:
            messagebox.showerror("Error", "Debe seleccionar un cargo.")
            return
        cargo = self.list_cargo.get(seleccion_cargo[0])

        # Género
        if self.var_masculino.get() == 1 and self.var_femenino.get() == 0:
            genero = "Masculino"
        elif self.var_masculino.get() == 0 and self.var_femenino.get() == 1:
            genero = "Femenino"
        else:
            messagebox.showerror("Error", "Debe seleccionar exactamente un género.")
            return

        # Salario día
        salario_dia = self._parse_float(self.entry_salario_dia, "Salario por día", obligatorio=True)
        if salario_dia is None:
            return

        # Días trabajados
        try:
            dias_trabajados = int(self.var_dias.get())
            if dias_trabajados < 1 or dias_trabajados > 31:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Los días trabajados deben estar entre 1 y 31.")
            return

        # Otros campos
        otros_ingresos = self._parse_float(self.entry_otros_ingresos, "Otros ingresos", obligatorio=False)
        if otros_ingresos is None:
            return

        pagos_salud = self._parse_float(self.entry_pagos_salud, "Pagos por salud", obligatorio=False)
        if pagos_salud is None:
            return

        aporte_pension = self._parse_float(self.entry_aporte_pension, "Aporte pensiones", obligatorio=False)
        if aporte_pension is None:
            return

        empleado = Empleado(
            nombre=nombre,
            apellidos=apellidos,
            cargo=cargo,
            genero=genero,
            salario_dia=salario_dia,
            dias_trabajados=dias_trabajados,
            otros_ingresos=otros_ingresos,
            pagos_salud=pagos_salud,
            aporte_pension=aporte_pension
        )

        self.lista_empleados.append(empleado)
        messagebox.showinfo("Información", "Empleado agregado correctamente.")

        # Limpiar campos para permitir agregar otro
        self._limpiar_campos()

    def _limpiar_campos(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellidos.delete(0, tk.END)
        self.list_cargo.selection_clear(0, tk.END)
        self.var_masculino.set(0)
        self.var_femenino.set(0)
        self.entry_salario_dia.delete(0, tk.END)
        self.var_dias.set(1)
        self.entry_otros_ingresos.delete(0, tk.END)
        self.entry_pagos_salud.delete(0, tk.END)
        self.entry_aporte_pension.delete(0, tk.END)


class NominaWindow(tk.Toplevel):
    """Ventana que muestra la tabla de nómina y el total."""

    def __init__(self, master, lista_empleados):
        super().__init__(master)
        self.title("Nómina de empleados")
        self.lista_empleados = lista_empleados

        self.geometry("600x400")
        self.resizable(True, True)
        self._crear_widgets()

    def _crear_widgets(self):
        columnas = ("nombre", "apellidos", "salario")
        tree = ttk.Treeview(self, columns=columnas, show="headings")
        tree.heading("nombre", text="Nombre")
        tree.heading("apellidos", text="Apellidos")
        tree.heading("salario", text="Salario mensual")

        tree.column("nombre", width=150)
        tree.column("apellidos", width=200)
        tree.column("salario", width=120, anchor="e")

        scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar_y.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        total_nomina = 0.0
        for emp in self.lista_empleados:
            salario_mensual = emp.calcular_salario_mensual()
            total_nomina += salario_mensual
            tree.insert(
                "", tk.END,
                values=(emp.nombre, emp.apellidos, f"{salario_mensual:.2f}")
            )

        lbl_total = tk.Label(
            self,
            text=f"Total de la nómina: {total_nomina:.2f}",
            anchor="e"
        )
        lbl_total.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=5)


class NominaApp(tk.Tk):
    """Ventana principal de la aplicación."""

    def __init__(self):
        super().__init__()
        self.title("Gestión de Nómina")
        self.geometry("600x400")
        self.resizable(True, True)

        self.empleados = []

        self._crear_menu()
        self._crear_contenido_principal()

    def _crear_menu(self):
        menubar = tk.Menu(self)

        menu_opciones = tk.Menu(menubar, tearoff=0)
        menu_opciones.add_command(label="Agregar empleado", command=self._abrir_agregar_empleado)
        menu_opciones.add_command(label="Calcular nómina", command=self._abrir_nomina)
        menu_opciones.add_separator()
        menu_opciones.add_command(label="Guardar archivo", command=self._guardar_archivo)

        menubar.add_cascade(label="Opciones", menu=menu_opciones)

        self.config(menu=menubar)

    def _crear_contenido_principal(self):
        lbl = tk.Label(
            self,
            text="Use la barra de menús para agregar empleados,\ncalcular la nómina y guardar el archivo.",
            justify="center"
        )
        lbl.pack(expand=True)

    def _abrir_agregar_empleado(self):
        AgregarEmpleadoWindow(self, self.empleados)

    def _abrir_nomina(self):
        if not self.empleados:
            messagebox.showinfo("Información", "No hay empleados registrados.")
            return
        NominaWindow(self, self.empleados)

    def _guardar_archivo(self):
        if not self.empleados:
            messagebox.showinfo("Información", "No hay empleados para guardar.")
            return

        carpeta = filedialog.askdirectory(
            title="Seleccione la carpeta donde se guardará Nómina.txt"
        )
        if not carpeta:
            return  # Usuario canceló

        ruta_archivo = os.path.join(carpeta, "Nómina.txt")

        try:
            total_nomina = 0.0
            with open(ruta_archivo, "w", encoding="utf-8") as f:
                f.write("NÓMINA DE EMPLEADOS\n")
                f.write("------------------------------------------------------\n")
                for emp in self.empleados:
                    salario_mensual = emp.calcular_salario_mensual()
                    total_nomina += salario_mensual
                    linea = (
                        f"Nombre: {emp.nombre} {emp.apellidos} | "
                        f"Cargo: {emp.cargo} | Género: {emp.genero} | "
                        f"Salario mensual: {salario_mensual:.2f}\n"
                    )
                    f.write(linea)
                f.write("------------------------------------------------------\n")
                f.write(f"TOTAL NÓMINA: {total_nomina:.2f}\n")

            messagebox.showinfo(
                "Éxito",
                f"Archivo guardado correctamente en:\n{ruta_archivo}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el archivo:\n{e}")


if __name__ == "__main__":
    app = NominaApp()
    app.mainloop()
