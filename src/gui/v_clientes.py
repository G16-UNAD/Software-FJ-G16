# src/gui/v_clientes.py
import tkinter as tk
from tkinter import ttk, messagebox
from src.cliente import Cliente
from src.exceptions import ClienteInvalidoError
from src.logger import logger


class ClientesView(tk.Frame):
    """Vista para la gestión de clientes.
    Permite crear, listar y validar clientes mediante un formulario dinámico.
    Los datos se almacenan en memoria en ``controller.base_datos_clientes``.
    """

    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg_color)
        self.controller = controller

        # Título
        tk.Label(
            self,
            text="Gestión de Clientes",
            font=("Helvetica", 18, "bold"),
            bg=controller.bg_color,
            fg=controller.text_dark,
        ).pack(anchor="w", pady=(0, 20))

        # Contenedor principal
        self.main_container = tk.Frame(self, bg=controller.bg_color)
        self.main_container.pack(fill="both", expand=True)

        self.crear_formulario()
        self.crear_tabla()
        self.actualizar_tabla()

    # ---------------------------------------------------------------------
    # Formulario de creación de cliente
    # ---------------------------------------------------------------------
    def crear_formulario(self):
        self.frame_form = tk.LabelFrame(
            self.main_container,
            text="Registrar nuevo cliente",
            font=("Helvetica", 11, "bold"),
            bg=self.controller.bg_color,
            fg=self.controller.text_dark,
            padx=15,
            pady=15,
        )
        self.frame_form.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Nombre
        tk.Label(
            self.frame_form,
            text="Nombre completo:",
            bg=self.controller.bg_color,
            fg=self.controller.text_dark,
        ).pack(anchor="w", pady=(5, 2))
        self.ent_nombre = tk.Entry(self.frame_form, font=("Helvetica", 10))
        self.ent_nombre.pack(fill="x", pady=(0, 8))

        # Email
        tk.Label(
            self.frame_form,
            text="Correo electrónico:",
            bg=self.controller.bg_color,
            fg=self.controller.text_dark,
        ).pack(anchor="w", pady=(5, 2))
        self.ent_email = tk.Entry(self.frame_form, font=("Helvetica", 10))
        self.ent_email.pack(fill="x", pady=(0, 8))

        # Teléfono
        tk.Label(
            self.frame_form,
            text="Teléfono (solo números):",
            bg=self.controller.bg_color,
            fg=self.controller.text_dark,
        ).pack(anchor="w", pady=(5, 2))
        self.ent_telefono = tk.Entry(self.frame_form, font=("Helvetica", 10))
        self.ent_telefono.pack(fill="x", pady=(0, 8))

        # Identificación
        tk.Label(
            self.frame_form,
            text="Identificación (cédula o NIT):",
            bg=self.controller.bg_color,
            fg=self.controller.text_dark,
        ).pack(anchor="w", pady=(5, 2))
        self.ent_identificacion = tk.Entry(self.frame_form, font=("Helvetica", 10))
        self.ent_identificacion.pack(fill="x", pady=(0, 8))

        # Botón crear
        btn_crear = tk.Button(
            self.frame_form,
            text="Crear Cliente",
            command=self.crear_cliente,
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

    # ---------------------------------------------------------------------
    # Tabla de visualización
    # ---------------------------------------------------------------------
    def crear_tabla(self):
        frame_tabla = tk.LabelFrame(
            self.main_container,
            text="Clientes Registrados",
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
            columns=("ID", "Nombre", "Email", "Teléfono", "Identificación"),
            show="headings",
            yscrollcommand=scroll.set,
        )
        self.tabla.pack(fill="both", expand=True)
        scroll.config(command=self.tabla.yview)

        # Encabezados
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Email", text="Email")
        self.tabla.heading("Teléfono", text="Teléfono")
        self.tabla.heading("Identificación", text="Identificación")

        # Anchos de columnas
        self.tabla.column("ID", width=80, anchor="center")
        self.tabla.column("Nombre", width=150, anchor="w")
        self.tabla.column("Email", width=180, anchor="w")
        self.tabla.column("Teléfono", width=120, anchor="center")
        self.tabla.column("Identificación", width=120, anchor="center")

    # ---------------------------------------------------------------------
    # Lógica de creación de cliente
    # ---------------------------------------------------------------------
    def crear_cliente(self):
        nombre = self.ent_nombre.get().strip()
        email = self.ent_email.get().strip()
        telefono = self.ent_telefono.get().strip()
        identificacion = self.ent_identificacion.get().strip()

        try:
            if not (nombre and email and telefono and identificacion):
                raise ClienteInvalidoError("Todos los campos son obligatorios.")

            cliente = Cliente(nombre, email, telefono, identificacion)
            self.controller.base_datos_clientes.append(cliente)
            logger.info(f"Cliente creado en GUI. ID: {cliente.id}")
            messagebox.showinfo("Cliente Registrado", "Cliente creado con éxito.")
            self.limpiar_formulario()
            self.actualizar_tabla()
        except ClienteInvalidoError as e:
            logger.warning(f"Error de validación al crear cliente: {e}")
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            logger.error(f"Error inesperado al crear cliente: {e}")
            messagebox.showerror("Error Inesperado", f"Ocurrió un error al registrar el cliente: {e}")

    def limpiar_formulario(self):
        self.ent_nombre.delete(0, tk.END)
        self.ent_email.delete(0, tk.END)
        self.ent_telefono.delete(0, tk.END)
        self.ent_identificacion.delete(0, tk.END)

    # ---------------------------------------------------------------------
    # Actualizar tabla de clientes
    # ---------------------------------------------------------------------
    def actualizar_tabla(self):
        # Limpiar tabla
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        # Insertar datos
        for cliente in self.controller.base_datos_clientes:
            id_corto = cliente.id[-8:]
            self.tabla.insert(
                "",
                "end",
                values=(
                    id_corto,
                    cliente.nombre,
                    cliente.email,
                    cliente.telefono,
                    cliente.identificacion,
                ),
            )

