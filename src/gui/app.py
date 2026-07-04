# src/gui/app.py
import tkinter as tk
from tkinter import ttk
from src.logger import logger
from src.gui.v_clientes import ClientesView
from src.gui.v_servicios import ServiciosView
from src.gui.v_reservas import ReservasView
from src.gui.v_logs import LogsView


class ApplicationGUI:
    """Ventana principal de la aplicación con sidebar y contenedor dinámico.

    Gestiona la navegación entre las vistas Cliente, Servicio, Reserva y Logs.
    Utiliza una paleta de colores premium y micro‑animaciones de hover.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Software FJ - Sistema Integral de Gestión")
        self.root.geometry("950x650")
        self.root.minsize(850, 550)
        self.root.configure(bg="#F3F4F6")

        # ---------- Paleta de colores ----------
        self.bg_color = "#F3F4F6"
        self.sidebar_color = "#1E293B"
        self.accent_color = "#3B82F6"
        self.text_light = "#F8FAFC"
        self.text_dark = "#0F172A"

        # ---------- Mock DB ----------
        self.base_datos_clientes = []
        self.base_datos_servicios = []
        self.base_datos_reservas = []

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.crear_sidebar()
        self.crear_contenedor_principal()

        self.vistas = {}
        self.vista_actual = None
        self.vista_actual_nombre = ""

        # Vista inicial: pantalla de bienvenida (ningún módulo seleccionado por defecto)
        self.mostrar_vista("bienvenida")
        logger.info("Aplicación GUI iniciada correctamente.")

    # ---------- Sidebar ----------
    def crear_sidebar(self):
        self.sidebar = tk.Frame(self.root, bg=self.sidebar_color, width=240)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Título del sidebar
        tk.Label(
            self.sidebar,
            text="Software FJ",
            font=("Helvetica", 20, "bold"),
            bg=self.sidebar_color,
            fg=self.text_light,
        ).pack(pady=(35, 5), padx=10)

        tk.Label(
            self.sidebar,
            text="Gestión de Reservas",
            font=("Helvetica", 10, "italic"),
            bg=self.sidebar_color,
            fg="#94A3B8",
        ).pack(pady=(0, 35))

        # Botones de navegación
        self.btn_clientes = self.crear_boton_navegacion(
            "Clientes", lambda: self.mostrar_vista("clientes")
        )
        self.btn_servicios = self.crear_boton_navegacion(
            "Servicios", lambda: self.mostrar_vista("servicios")
        )
        self.btn_reservas = self.crear_boton_navegacion(
            "Reservas", lambda: self.mostrar_vista("reservas")
        )
        self.btn_logs = self.crear_boton_navegacion(
            "Logs y Simulación", lambda: self.mostrar_vista("logs")
        )

    def crear_boton_navegacion(self, texto, comando):
        btn = tk.Button(
            self.sidebar,
            text=texto,
            command=comando,
            font=("Helvetica", 11, "bold"),
            bg=self.sidebar_color,
            fg=self.text_light,
            activebackground=self.accent_color,
            activeforeground=self.text_light,
            bd=0,
            relief="flat",
            height=2,
            anchor="w",
            padx=25,
            cursor="hand2",
        )
        btn.pack(fill="x", pady=3)
        # Hover efectos
        btn.bind(
            "<Enter>",
            lambda e: btn.configure(bg="#334155")
            if self.vista_actual_nombre != texto.lower().split()[0]
            else None,
        )
        btn.bind(
            "<Leave>",
            lambda e: btn.configure(bg=self.sidebar_color)
            if self.vista_actual_nombre != texto.lower().split()[0]
            else None,
        )
        return btn

    # ---------- Contenedor principal ----------
    def crear_contenedor_principal(self):
        self.contenedor = tk.Frame(self.root, bg=self.bg_color)
        self.contenedor.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.contenedor.grid_columnconfigure(0, weight=1)
        self.contenedor.grid_rowconfigure(0, weight=1)

    # ---------- Navegación ----------
    def mostrar_vista(self, nombre_vista):
        self.vista_actual_nombre = nombre_vista
        # Reset colores de los botones.
        for btn in (self.btn_clientes, self.btn_servicios, self.btn_reservas, self.btn_logs):
            btn.configure(bg=self.sidebar_color)
        if self.vista_actual:
            self.vista_actual.pack_forget()
        if nombre_vista == "clientes":
            self.btn_clientes.configure(bg=self.accent_color)
            self.vista_actual = self._obtener_o_crear_vista("clientes", ClientesView)
        elif nombre_vista == "servicios":
            self.btn_servicios.configure(bg=self.accent_color)
            self.vista_actual = self._obtener_o_crear_vista("servicios", ServiciosView)
        elif nombre_vista == "reservas":
            self.btn_reservas.configure(bg=self.accent_color)
            self.vista_actual = self._obtener_o_crear_vista("reservas", ReservasView)
        elif nombre_vista == "logs":
            self.btn_logs.configure(bg=self.accent_color)
            self.vista_actual = self._obtener_o_crear_vista("logs", LogsView)
        elif nombre_vista == "bienvenida":
            self.vista_actual = self._obtener_o_crear_vista("bienvenida", BienvenidaView)

        # Refrescar datos dinámicamente al cambiar de pestaña
        if hasattr(self.vista_actual, "actualizar_tabla"):
            self.vista_actual.actualizar_tabla()
        elif hasattr(self.vista_actual, "cargar_logs"):
            self.vista_actual.cargar_logs()

        self.vista_actual.pack(fill="both", expand=True)

    def _obtener_o_crear_vista(self, clave, clase_vista):
        if clave not in self.vistas:
            self.vistas[clave] = clase_vista(self.contenedor, self)
        return self.vistas[clave]


class BienvenidaView(tk.Frame):
    """Vista de bienvenida mostrada al iniciar la aplicación."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg_color)

        # Contenedor central
        lbl_titulo = tk.Label(
            self,
            text="¡Bienvenido a Software FJ!",
            font=("Helvetica", 24, "bold"),
            bg=controller.bg_color,
            fg=controller.text_dark
        )
        lbl_titulo.pack(pady=(150, 10))

        lbl_instruccion = tk.Label(
            self,
            text="Seleccione uno de los módulos de la barra lateral izquierda\npara comenzar a administrar clientes, servicios y reservas.",
            font=("Helvetica", 12),
            bg=controller.bg_color,
            fg="#475569",
            justify="center"
        )
        lbl_instruccion.pack(pady=10)

        lbl_logo = tk.Label(
            self,
            text="🚀",
            font=("Helvetica", 64),
            bg=controller.bg_color
        )
        lbl_logo.pack(pady=20)


def iniciar_app():
    root = tk.Tk()
    ApplicationGUI(root)
    root.mainloop()
