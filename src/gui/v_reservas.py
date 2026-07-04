# src/gui/v_reservas.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.reserva import Reserva
from src.exceptions import ReservaInvalidaError
from src.logger import logger
from src.gui.utils import formatear_moneda_cop


class ReservasView(tk.Frame):
    """Vista para la gestión de reservas.
    Permite crear una reserva vinculando cliente y servicio, y luego
    confirmar o cancelar la reserva. Todos los objetos se almacenan en
    ``controller.base_datos_reservas``.
    """

    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg_color)
        self.controller = controller

        tk.Label(
            self,
            text="Gestión de Reservas",
            font=("Helvetica", 18, "bold"),
            bg=controller.bg_color,
            fg=controller.text_dark,
        ).pack(anchor="w", pady=(0, 20))

        self.main_container = tk.Frame(self, bg=controller.bg_color)
        self.main_container.pack(fill="both", expand=True)

        self.crear_formulario()
        self.crear_tabla()
        self.actualizar_tabla()

    # ------------------------------------------------------------------
    # Formulario de creación de reserva
    # ------------------------------------------------------------------
    def crear_formulario(self):
        self.frame_form = tk.LabelFrame(
            self.main_container,
            text="Crear nueva reserva",
            font=("Helvetica", 11, "bold"),
            bg=self.controller.bg_color,
            fg=self.controller.text_dark,
            padx=15,
            pady=15,
        )
        self.frame_form.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Cliente selector
        tk.Label(
            self.frame_form,
            text="Cliente:",
            bg=self.controller.bg_color,
            fg=self.controller.text_dark,
        ).pack(anchor="w", pady=(5, 2))
        self.combo_cliente = ttk.Combobox(
            self.frame_form, state="readonly", font=("Helvetica", 10)
        )
        self.combo_cliente.pack(fill="x", pady=(0, 8))

        # Servicio selector
        tk.Label(
            self.frame_form,
            text="Servicio:",
            bg=self.controller.bg_color,
            fg=self.controller.text_dark,
        ).pack(anchor="w", pady=(5, 2))
        self.combo_servicio = ttk.Combobox(
            self.frame_form, state="readonly", font=("Helvetica", 10)
        )
        self.combo_servicio.pack(fill="x", pady=(0, 8))

        # Fecha y Hora (DD/MM/YYYY HH:MM)
        tk.Label(
            self.frame_form,
            text="Fecha y Hora (DD/MM/YYYY HH:MM):",
            bg=self.controller.bg_color,
            fg=self.controller.text_dark,
        ).pack(anchor="w", pady=(5, 2))
        self.ent_fecha = tk.Entry(self.frame_form, font=("Helvetica", 10))
        self.ent_fecha.pack(fill="x", pady=(0, 8))

        # Botón crear reserva
        btn_crear = tk.Button(
            self.frame_form,
            text="Crear Reserva",
            command=self.crear_reserva,
            font=("Helvetica", 10, "bold"),
            bg=self.controller.accent_color,
            fg=self.controller.text_light,
            activebackground="#2563EB",
            activeforeground=self.controller.text_light,
            bd=0,
            height=2,
            cursor="hand2",
        )
        btn_crear.pack(fill="x", side="bottom", pady=(10, 0))

    # ------------------------------------------------------------------
    # Tabla de reservas
    # ------------------------------------------------------------------
    def crear_tabla(self):
        frame_tabla = tk.LabelFrame(
            self.main_container,
            text="Reservas Registradas",
            font=("Helvetica", 11, "bold"),
            bg=self.controller.bg_color,
            fg=self.controller.text_dark,
            padx=10,
            pady=10,
        )
        frame_tabla.pack(side="right", fill="both", expand=True, padx=(10, 0))

        scroll = ttk.Scrollbar(frame_tabla)
        scroll.pack(side="right", fill="y")

        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=("ID", "Cliente", "Servicio", "Fecha", "Estado", "CostoFinal"),
            show="headings",
            yscrollcommand=scroll.set,
        )
        self.tabla.pack(fill="both", expand=True)
        scroll.config(command=self.tabla.yview)

        lbl_instruccion = tk.Label(
            frame_tabla,
            text="💡 Nota: Haga doble clic sobre una reserva en la lista para Confirmarla o Cancelarla.",
            font=("Helvetica", 9, "italic"),
            bg=self.controller.bg_color,
            fg="#4B5563"
        )
        lbl_instruccion.pack(side="bottom", fill="x", pady=(5, 0))

        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Cliente", text="Cliente")
        self.tabla.heading("Servicio", text="Servicio")
        self.tabla.heading("Fecha", text="Fecha")
        self.tabla.heading("Estado", text="Estado")
        self.tabla.heading("CostoFinal", text="Costo Final")

        self.tabla.column("ID", width=80, anchor="center")
        self.tabla.column("Cliente", width=150, anchor="w")
        self.tabla.column("Servicio", width=150, anchor="w")
        self.tabla.column("Fecha", width=100, anchor="center")
        self.tabla.column("Estado", width=100, anchor="center")
        self.tabla.column("CostoFinal", width=120, anchor="center")

        self.tabla.bind("<Double-1>", self.mostrar_opciones_reserva)

    # ------------------------------------------------------------------
    # Lógica de creación y acciones de reserva
    # ------------------------------------------------------------------
    def actualizar_combos(self):
        # Clientes
        clientes = [f"{c.nombre} ({c.id[-8:]})" for c in self.controller.base_datos_clientes]
        self.combo_cliente['values'] = clientes
        val_cliente = self.combo_cliente.get()
        if val_cliente not in clientes:
            self.combo_cliente.set("")

        # Servicios
        servicios = [f"{s.nombre_servicio} ({s.id[-8:]})" for s in self.controller.base_datos_servicios]
        self.combo_servicio['values'] = servicios
        val_servicio = self.combo_servicio.get()
        if val_servicio not in servicios:
            self.combo_servicio.set("")

    def crear_reserva(self):
        # Obtener índices
        try:
            idx_cliente = self.combo_cliente.current()
            idx_servicio = self.combo_servicio.current()
            if idx_cliente == -1 or idx_servicio == -1:
                raise ReservaInvalidaError("Debe seleccionar cliente y servicio.")
            cliente = self.controller.base_datos_clientes[idx_cliente]
            servicio = self.controller.base_datos_servicios[idx_servicio]
            fecha_str = self.ent_fecha.get().strip()
            if not fecha_str:
                raise ReservaInvalidaError("La fecha es obligatoria.")
            fecha = datetime.strptime(fecha_str, "%d/%m/%Y %H:%M")

            reserva = Reserva(cliente, servicio, fecha)
            self.controller.base_datos_reservas.append(reserva)
            logger.info(f"Reserva creada en GUI. ID: {reserva.id}")
            messagebox.showinfo("Reserva Creada", "Reserva registrada con éxito.")
            self.limpiar_formulario()
            self.actualizar_tabla()
        except ReservaInvalidaError as e:
            logger.warning(f"Error al crear reserva: {e}")
            messagebox.showerror("Error de Validación", str(e))
        except ValueError as e:
            logger.warning(f"Formato de fecha incorrecto: {e}")
            messagebox.showerror("Error de Fecha", "Use formato DD/MM/YYYY HH:MM.")
        except Exception as e:
            logger.error(f"Error inesperado al crear reserva: {e}")
            messagebox.showerror("Error Inesperado", f"{e}")

    def limpiar_formulario(self):
        self.ent_fecha.delete(0, tk.END)
        self.combo_cliente.set("")
        self.combo_servicio.set("")

    # ------------------------------------------------------------------
    # Interacción con tabla (doble click)
    # ------------------------------------------------------------------
    def mostrar_opciones_reserva(self, event):
        item_id = self.tabla.focus()
        if not item_id:
            return
        reserva_index = int(self.tabla.item(item_id, "text")) 
        reserva = self.controller.base_datos_reservas[reserva_index]

        top = tk.Toplevel(self)
        top.title("Acciones Reserva")
        top.geometry("300x150")
        top.configure(bg=self.controller.bg_color)

        tk.Label(
            top,
            text=f"Reserva {reserva.id[-8:]}",
            font=("Helvetica", 12, "bold"),
            bg=self.controller.bg_color,
            fg=self.controller.text_dark,
        ).pack(pady=10)

        btn_confirmar = tk.Button(
            top,
            text="Confirmar",
            command=lambda: self._accion_reserva(reserva, "confirmar", top),
            bg=self.controller.accent_color,
            fg=self.controller.text_light,
            width=12,
        )
        btn_confirmar.pack(pady=5)

        btn_cancelar = tk.Button(
            top,
            text="Cancelar",
            command=lambda: self._accion_reserva(reserva, "cancelar", top),
            bg="#DC2626",
            fg=self.controller.text_light,
            width=12,
        )
        btn_cancelar.pack(pady=5)

    def _accion_reserva(self, reserva, accion, ventana):
        try:
            if accion == "confirmar":
                reserva.confirmar()
                logger.info(f"Reserva {reserva.id} confirmada desde GUI.")
                costo_final_str = formatear_moneda_cop(reserva.costo_final)
                messagebox.showinfo("Confirmado", f"Reserva confirmada con éxito.\nCosto Total: {costo_final_str}")
            elif accion == "cancelar":
                reserva.cancelar()
                logger.info(f"Reserva {reserva.id} cancelada desde GUI.")
                messagebox.showinfo("Cancelado", "Reserva cancelada.")
            self.actualizar_tabla()
        except ReservaInvalidaError as e:
            logger.warning(f"Operación reserva falló: {e}")
            messagebox.showerror("Error", str(e))
        finally:
            ventana.destroy()

    # ------------------------------------------------------------------
    # Actualizar tabla de reservas
    # ------------------------------------------------------------------
    def actualizar_tabla(self):
        self.actualizar_combos()

        for row in self.tabla.get_children():
            self.tabla.delete(row)

        for idx, reserva in enumerate(self.controller.base_datos_reservas):
            id_corto = reserva.id[-8:]
            cliente_nombre = reserva.cliente.nombre
            servicio_nombre = reserva.servicio.nombre_servicio
            fecha_str = reserva.fecha_reserva.strftime("%d/%m/%Y %H:%M")
            estado = reserva.estado
            costo_str = formatear_moneda_cop(reserva.costo_final) if estado == "CONFIRMADA" else "-"
            self.tabla.insert(
                "",
                "end",
                text=str(idx),
                values=(id_corto, cliente_nombre, servicio_nombre, fecha_str, estado, costo_str),
            )
