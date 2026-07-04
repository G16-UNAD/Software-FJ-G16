import tkinter as tk
from tkinter import ttk, messagebox
from src.servicios.sala import ReservaSala
from src.servicios.equipo import AlquilerEquipos
from src.servicios.asesoria import AsesoriaEspecializada
from src.exceptions import ServicioInvalidoError
from src.logger import logger
from src.gui.utils import limpiar_y_parsear_costo, formatear_moneda_cop

class ServiciosView(tk.Frame):
    """
    Vista de administración de Servicios.
    Permite registrar Reservas de Salas, Alquiler de Equipos o Asesorías Especializadas
    utilizando formularios dinámicos según el tipo de servicio y listarlos en una tabla Treeview.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg_color)
        self.controller = controller
        
        # Título de la sección
        lbl_titulo = tk.Label(
            self, 
            text="Administración de Servicios", 
            font=("Helvetica", 18, "bold"), 
            bg=controller.bg_color, 
            fg=controller.text_dark
        )
        lbl_titulo.pack(anchor="w", pady=(0, 20))

        # Contenedor principal
        self.main_container = tk.Frame(self, bg=controller.bg_color)
        self.main_container.pack(fill="both", expand=True)

        self.crear_formulario()
        self.crear_tabla()
        
        # Mostrar inputs iniciales correspondientes a ReservaSala
        self.cambiar_tipo_servicio()
        self.actualizar_tabla()

    def crear_formulario(self):
        self.frame_form = tk.LabelFrame(
            self.main_container, 
            text="Registrar Nuevo Servicio", 
            font=("Helvetica", 11, "bold"), 
            bg=self.controller.bg_color, 
            fg=self.controller.text_dark, 
            padx=15, 
            pady=15
        )
        self.frame_form.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Selector de Tipo de Servicio
        tk.Label(self.frame_form, text="Tipo de Servicio:", bg=self.controller.bg_color, fg=self.controller.text_dark).pack(anchor="w", pady=(5, 2))
        self.combo_tipo = ttk.Combobox(
            self.frame_form, 
            values=["Reserva de Sala", "Alquiler de Equipos", "Asesoría Especializada"], 
            state="readonly",
            font=("Helvetica", 10)
        )
        self.combo_tipo.set("Reserva de Sala")
        self.combo_tipo.pack(fill="x", pady=(0, 15))
        self.combo_tipo.bind("<<ComboboxSelected>>", lambda e: self.cambiar_tipo_servicio())

        # Contenedor para inputs dinámicos
        self.frame_dinamico = tk.Frame(self.frame_form, bg=self.controller.bg_color)
        self.frame_dinamico.pack(fill="both", expand=True, pady=(0, 15))

        # Botón de envío
        btn_crear = tk.Button(
            self.frame_form, 
            text="Crear Servicio", 
            command=self.crear_servicio, 
            font=("Helvetica", 10, "bold"), 
            bg=self.controller.accent_color, 
            fg=self.controller.text_light, 
            activebackground="#2563EB", 
            activeforeground=self.controller.text_light, 
            bd=0, 
            height=2, 
            cursor="hand2"
        )
        btn_crear.pack(fill="x", side="bottom")

    def cambiar_tipo_servicio(self):
        """Modifica dinámicamente los campos del formulario según la selección del Combobox."""
        # Limpiar inputs viejos
        for widget in self.frame_dinamico.winfo_children():
            widget.destroy()

        tipo = self.combo_tipo.get()

        if tipo == "Reserva de Sala":
            tk.Label(self.frame_dinamico, text="Tipo de Sala (ej: Reunión, Conferencia):", bg=self.controller.bg_color, fg=self.controller.text_dark).pack(anchor="w", pady=2)
            self.ent_param1 = tk.Entry(self.frame_dinamico, font=("Helvetica", 10))
            self.ent_param1.pack(fill="x", pady=(0, 8))

            tk.Label(self.frame_dinamico, text="Capacidad de Personas:", bg=self.controller.bg_color, fg=self.controller.text_dark).pack(anchor="w", pady=2)
            self.ent_param2 = tk.Entry(self.frame_dinamico, font=("Helvetica", 10))
            self.ent_param2.pack(fill="x", pady=(0, 8))

            tk.Label(self.frame_dinamico, text="Horas Reservadas:", bg=self.controller.bg_color, fg=self.controller.text_dark).pack(anchor="w", pady=2)
            self.ent_param3 = tk.Entry(self.frame_dinamico, font=("Helvetica", 10))
            self.ent_param3.pack(fill="x", pady=(0, 8))

            tk.Label(self.frame_dinamico, text="Costo Base por Hora ($):", bg=self.controller.bg_color, fg=self.controller.text_dark).pack(anchor="w", pady=2)
            self.ent_costo = tk.Entry(self.frame_dinamico, font=("Helvetica", 10))
            self.ent_costo.pack(fill="x", pady=(0, 8))

        elif tipo == "Alquiler de Equipos":
            tk.Label(self.frame_dinamico, text="Nombre del Equipo (ej: Laptop, Proyector):", bg=self.controller.bg_color, fg=self.controller.text_dark).pack(anchor="w", pady=2)
            self.ent_param1 = tk.Entry(self.frame_dinamico, font=("Helvetica", 10))
            self.ent_param1.pack(fill="x", pady=(0, 8))

            tk.Label(self.frame_dinamico, text="Cantidad de Equipos:", bg=self.controller.bg_color, fg=self.controller.text_dark).pack(anchor="w", pady=2)
            self.ent_param2 = tk.Entry(self.frame_dinamico, font=("Helvetica", 10))
            self.ent_param2.pack(fill="x", pady=(0, 8))

            tk.Label(self.frame_dinamico, text="Días de Alquiler:", bg=self.controller.bg_color, fg=self.controller.text_dark).pack(anchor="w", pady=2)
            self.ent_param3 = tk.Entry(self.frame_dinamico, font=("Helvetica", 10))
            self.ent_param3.pack(fill="x", pady=(0, 8))

            tk.Label(self.frame_dinamico, text="Costo de Alquiler por Día ($):", bg=self.controller.bg_color, fg=self.controller.text_dark).pack(anchor="w", pady=2)
            self.ent_costo = tk.Entry(self.frame_dinamico, font=("Helvetica", 10))
            self.ent_costo.pack(fill="x", pady=(0, 8))

        elif tipo == "Asesoría Especializada":
            tk.Label(self.frame_dinamico, text="Tema de Asesoría (ej: Software, Redes):", bg=self.controller.bg_color, fg=self.controller.text_dark).pack(anchor="w", pady=2)
            self.ent_param1 = tk.Entry(self.frame_dinamico, font=("Helvetica", 10))
            self.ent_param1.pack(fill="x", pady=(0, 8))

            tk.Label(self.frame_dinamico, text="Nombre del Consultor:", bg=self.controller.bg_color, fg=self.controller.text_dark).pack(anchor="w", pady=2)
            self.ent_param2 = tk.Entry(self.frame_dinamico, font=("Helvetica", 10))
            self.ent_param2.pack(fill="x", pady=(0, 8))

            tk.Label(self.frame_dinamico, text="Horas Planificadas:", bg=self.controller.bg_color, fg=self.controller.text_dark).pack(anchor="w", pady=2)
            self.ent_param3 = tk.Entry(self.frame_dinamico, font=("Helvetica", 10))
            self.ent_param3.pack(fill="x", pady=(0, 8))

            tk.Label(self.frame_dinamico, text="Tarifa Base por Hora ($):", bg=self.controller.bg_color, fg=self.controller.text_dark).pack(anchor="w", pady=2)
            self.ent_costo = tk.Entry(self.frame_dinamico, font=("Helvetica", 10))
            self.ent_costo.pack(fill="x", pady=(0, 8))

    def crear_tabla(self):
        frame_tabla = tk.LabelFrame(
            self.main_container, 
            text="Servicios Registrados", 
            font=("Helvetica", 11, "bold"), 
            bg=self.controller.bg_color, 
            fg=self.controller.text_dark, 
            padx=10, 
            pady=10
        )
        frame_tabla.pack(side="right", fill="both", expand=True, padx=(10, 0))

        scroll = ttk.Scrollbar(frame_tabla)
        scroll.pack(side="right", fill="y")

        self.tabla = ttk.Treeview(
            frame_tabla, 
            columns=("ID", "Tipo", "Detalles", "CostoBase"), 
            show="headings", 
            yscrollcommand=scroll.set
        )
        self.tabla.pack(fill="both", expand=True)
        scroll.config(command=self.tabla.yview)

        # Encabezados
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Tipo", text="Tipo")
        self.tabla.heading("Detalles", text="Detalles / Parámetros")
        self.tabla.heading("CostoBase", text="Costo Base ($)")

        # Ancho de columnas
        self.tabla.column("ID", width=80, anchor="center")
        self.tabla.column("Tipo", width=130, anchor="w")
        self.tabla.column("Detalles", width=250, anchor="w")
        self.tabla.column("CostoBase", width=100, anchor="center")

    def crear_servicio(self):
        tipo = self.combo_tipo.get()
        p1 = self.ent_param1.get()
        p2 = self.ent_param2.get()
        p3 = self.ent_param3.get()
        costo_str = self.ent_costo.get()

        try:
            # Validar costo numérico con soporte para formato colombiano
            try:
                costo = limpiar_y_parsear_costo(costo_str)
            except ValueError:
                raise ServicioInvalidoError("El costo base/tarifa debe ser un número decimal o entero válido (ej: 50.000 o 1.200.000).")

            if tipo == "Reserva de Sala":
                try:
                    capacidad = int(p2)
                    horas = int(p3)
                except ValueError:
                    raise ServicioInvalidoError("La capacidad de la sala y las horas de reserva deben ser enteros.")
                
                servicio = ReservaSala(p1, capacidad, horas, costo)

            elif tipo == "Alquiler de Equipos":
                try:
                    cantidad = int(p2)
                    dias = int(p3)
                except ValueError:
                    raise ServicioInvalidoError("La cantidad de equipos y los días de alquiler deben ser enteros.")
                
                servicio = AlquilerEquipos(p1, cantidad, dias, costo)

            elif tipo == "Asesoría Especializada":
                try:
                    horas = int(p3)
                except ValueError:
                    raise ServicioInvalidoError("Las horas planificadas de asesoría deben ser un número entero.")
                
                servicio = AsesoriaEspecializada(p1, p2, horas, costo)

            # Registrar servicio en base de datos en memoria del controlador
            self.controller.base_datos_servicios.append(servicio)
            logger.info(f"Servicio {tipo} creado en GUI. ID: {servicio.id}")
            messagebox.showinfo("Servicio Registrado", f"Servicio '{tipo}' registrado con éxito.")
            
            # Limpiar entradas y actualizar
            self.cambiar_tipo_servicio()
            self.actualizar_tabla()

        except ServicioInvalidoError as e:
            logger.warning(f"Error de validación al crear servicio en GUI: {e}")
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            logger.error(f"Error inesperado al crear servicio en GUI: {e}")
            messagebox.showerror("Error Inesperado", f"Ocurrió un error al registrar el servicio: {e}")

    def actualizar_tabla(self):
        # Limpiar
        for row in self.tabla.get_children():
            self.tabla.delete(row)
            
        # Agregar elementos
        for servicio in self.controller.base_datos_servicios:
            # Mostramos los últimos 8 caracteres para legibilidad
            id_corto = servicio.id[-8:]
            self.tabla.insert("", "end", values=(
                id_corto, 
                servicio.nombre_servicio, 
                servicio.obtener_descripcion(), 
                formatear_moneda_cop(servicio.costo_base)
            ))
