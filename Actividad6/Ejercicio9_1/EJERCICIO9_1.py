# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import datetime as dt
import calendar


class Contacto:
    """Clase que representa un contacto de la agenda."""

    def __init__(self, nombres, apellidos, fecha_nacimiento,
                 direccion, telefono, correo):
        self.nombres = nombres
        self.apellidos = apellidos
        self.fecha_nacimiento = fecha_nacimiento  # objeto date
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo

    def __str__(self):
        # Texto que se mostrará en la ListView (Listbox)
        fecha_txt = self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else "N/A"
        return (f"{self.nombres} {self.apellidos} | "
                f"F.Nac: {fecha_txt} | Tel: {self.telefono} | "
                f"Correo: {self.correo}")


class DatePicker(tk.Frame):
    """
    Componente DatePicker simple:
    - Muestra un Entry con la fecha en formato AAAA-MM-DD.
    - Botón que abre una ventana emergente con un calendario.
    """

    def __init__(self, master=None, fecha_inicial=None, **kwargs):
        super().__init__(master, **kwargs)

        if fecha_inicial is None:
            fecha_inicial = dt.date.today()

        self._fecha = fecha_inicial

        self.entry = tk.Entry(self, width=12)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self._actualizar_entry()

        btn = tk.Button(self, text="📅", width=3, command=self._abrir_calendario)
        btn.pack(side=tk.LEFT, padx=2)

    def _actualizar_entry(self):
        if self._fecha:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self._fecha.isoformat())

    def _abrir_calendario(self):
        CalendarPopup(self, self._fecha, self._set_fecha_desde_calendario)

    def _set_fecha_desde_calendario(self, fecha):
        self._fecha = fecha
        self._actualizar_entry()

    def get_date(self):
        """
        Devuelve la fecha seleccionada como objeto date.
        Si el usuario escribe manualmente, intenta parsearla.
        """
        texto = self.entry.get().strip()
        if not texto:
            return None
        try:
            return dt.datetime.strptime(texto, "%Y-%m-%d").date()
        except ValueError:
            # Si el formato es incorrecto, se devuelve None
            return None


class CalendarPopup(tk.Toplevel):
    """Ventana emergente con un calendario para seleccionar una fecha."""

    def __init__(self, master, fecha_inicial, callback):
        super().__init__(master)
        self.title("Seleccionar fecha")
        self.callback = callback

        self.geometry("260x240")
        self.resizable(False, False)
        self.grab_set()

        if fecha_inicial is None:
            fecha_inicial = dt.date.today()

        self.year = fecha_inicial.year
        self.month = fecha_inicial.month

        self._crear_widgets()
        self._mostrar_calendario()

    def _crear_widgets(self):
        top_frame = tk.Frame(self)
        top_frame.pack(fill=tk.X, pady=5)

        btn_prev = tk.Button(top_frame, text="<", width=3, command=self._mes_anterior)
        btn_prev.pack(side=tk.LEFT, padx=5)

        self.lbl_mes_anio = tk.Label(top_frame, text="", width=15)
        self.lbl_mes_anio.pack(side=tk.LEFT, expand=True)

        btn_next = tk.Button(top_frame, text=">", width=3, command=self._mes_siguiente)
        btn_next.pack(side=tk.RIGHT, padx=5)

        self.dias_frame = tk.Frame(self)
        self.dias_frame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

    def _mes_anterior(self):
        self.month -= 1
        if self.month == 0:
            self.month = 12
            self.year -= 1
        self._mostrar_calendario()

    def _mes_siguiente(self):
        self.month += 1
        if self.month == 13:
            self.month = 1
            self.year += 1
        self._mostrar_calendario()

    def _mostrar_calendario(self):
        for widget in self.dias_frame.winfo_children():
            widget.destroy()

        nombre_mes = calendar.month_name[self.month]
        self.lbl_mes_anio.config(text=f"{nombre_mes} {self.year}")

        # Encabezados de días
        dias_semana = ["Lu", "Ma", "Mi", "Ju", "Vi", "Sa", "Do"]
        for i, dia in enumerate(dias_semana):
            tk.Label(self.dias_frame, text=dia, width=3, borderwidth=1, relief="ridge").grid(row=0, column=i)

        cal = calendar.Calendar(firstweekday=0)  # lunes
        row = 1
        for week in cal.monthdayscalendar(self.year, self.month):
            for col, day in enumerate(week):
                if day == 0:
                    tk.Label(self.dias_frame, text="", width=3, borderwidth=1, relief="ridge").grid(row=row, column=col)
                else:
                    btn = tk.Button(
                        self.dias_frame, text=str(day), width=3,
                        command=lambda d=day: self._seleccionar_dia(d)
                    )
                    btn.grid(row=row, column=col, padx=1, pady=1)
            row += 1

    def _seleccionar_dia(self, day):
        fecha = dt.date(self.year, self.month, day)
        self.callback(fecha)
        self.destroy()


class AgendaApp(tk.Tk):
    """Ventana principal de la agenda de contactos."""

    def __init__(self):
        super().__init__()
        self.title("Agenda de contactos")
        self.geometry("600x400")
        self.resizable(True, True)

        self.contactos = []

        self._crear_widgets()

    def _crear_widgets(self):
        # Frame superior con el formulario
        frame_form = tk.Frame(self, padx=10, pady=10)
        frame_form.pack(fill=tk.X)

        # Nombres
        tk.Label(frame_form, text="Nombres:").grid(row=0, column=0, sticky="w")
        self.entry_nombres = tk.Entry(frame_form)
        self.entry_nombres.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        # Apellidos
        tk.Label(frame_form, text="Apellidos:").grid(row=1, column=0, sticky="w")
        self.entry_apellidos = tk.Entry(frame_form)
        self.entry_apellidos.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        # Fecha de nacimiento (DatePicker)
        tk.Label(frame_form, text="Fecha de nacimiento:").grid(row=2, column=0, sticky="w")
        self.datepicker_fnac = DatePicker(frame_form)
        self.datepicker_fnac.grid(row=2, column=1, sticky="w", padx=5, pady=2)

        # Dirección
        tk.Label(frame_form, text="Dirección:").grid(row=3, column=0, sticky="w")
        self.entry_direccion = tk.Entry(frame_form)
        self.entry_direccion.grid(row=3, column=1, sticky="ew", padx=5, pady=2)

        # Teléfono
        tk.Label(frame_form, text="Teléfono:").grid(row=4, column=0, sticky="w")
        self.entry_telefono = tk.Entry(frame_form)
        self.entry_telefono.grid(row=4, column=1, sticky="ew", padx=5, pady=2)

        # Correo
        tk.Label(frame_form, text="Correo electrónico:").grid(row=5, column=0, sticky="w")
        self.entry_correo = tk.Entry(frame_form)
        self.entry_correo.grid(row=5, column=1, sticky="ew", padx=5, pady=2)

        # Botón Agregar
        btn_agregar = tk.Button(frame_form, text="Agregar", command=self._agregar_contacto)
        btn_agregar.grid(row=6, column=0, columnspan=2, pady=10)

        frame_form.columnconfigure(1, weight=1)

        # Separador
        ttk.Separator(self, orient="horizontal").pack(fill=tk.X, pady=5)

        # ListView (Listbox) en la parte inferior
        frame_lista = tk.Frame(self, padx=10, pady=5)
        frame_lista.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame_lista, text="Contactos:").pack(anchor="w")

        self.listbox_contactos = tk.Listbox(frame_lista)
        self.listbox_contactos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_y = tk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.listbox_contactos.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_contactos.config(yscrollcommand=scrollbar_y.set)

    def _agregar_contacto(self):
        nombres = self.entry_nombres.get().strip()
        apellidos = self.entry_apellidos.get().strip()
        fecha_nac = self.datepicker_fnac.get_date()
        direccion = self.entry_direccion.get().strip()
        telefono = self.entry_telefono.get().strip()
        correo = self.entry_correo.get().strip()

        # Validaciones básicas (los campos de entrada son obligatorios)
        if not nombres or not apellidos or not direccion or not telefono or not correo:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if fecha_nac is None:
            messagebox.showerror("Error", "La fecha de nacimiento es obligatoria y debe tener formato AAAA-MM-DD.")
            return

        # Crear contacto y agregar a la lista
        contacto = Contacto(nombres, apellidos, fecha_nac, direccion, telefono, correo)
        self.contactos.append(contacto)
        self.listbox_contactos.insert(tk.END, str(contacto))

        # Opcional: limpiar campos
        self.entry_nombres.delete(0, tk.END)
        self.entry_apellidos.delete(0, tk.END)
        self.entry_direccion.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)

        messagebox.showinfo("Información", "Contacto agregado a la agenda.")


if __name__ == "__main__":
    app = AgendaApp()
    app.mainloop()
