import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from src.logger import logger

class ApplicationGUI:
    """
    Clase principal de la interfaz gráfica de usuario (GUI).
    Administra la ventana de Tkinter, el sidebar de navegación lateral y el contenedor de vistas.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Software FJ - Sistema Integral de Gestión")
        self.root.geometry("950x650")
        self.root.minsize(850, 550)
        self.root.configure(bg="#F3F4F6")

        # Configurar estilos generales
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Paleta de colores premium
        self.bg_color = "#F3F4F6"      # Gris claro para fondo
        self.sidebar_color = "#1E293B" # Azul oscuro pizarra
        self.accent_color = "#3B82F6"  # Azul brillante
        self.text_light = "#F8FAFC"    # Blanco/Gris muy claro
        self.text_dark = "#0F172A"     # Gris casi negro
        
        # Configurar grid de la ventana raíz
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Listas temporales de datos en memoria para compartir entre vistas (Mock DB)
        self.base_datos_clientes = []
        self.base_datos_servicios = []
        self.base_datos_reservas = []

        # Crear componentes visuales base
        self.crear_sidebar()
        self.crear_contenedor_principal()

        # Diccionario para almacenar las instancias de vistas
        self.vistas = {}
        self.vista_actual = None
        self.vista_actual_nombre = ""

        # Cargar vista inicial
        self.mostrar_vista("clientes")
        logger.info("Aplicación GUI de Software FJ iniciada correctamente.")

    def crear_sidebar(self):
        """Crea el panel de navegación lateral."""
        self.sidebar = tk.Frame(self.root, bg=self.sidebar_color, width=240)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Título del sidebar
        label_titulo = tk.Label(
            self.sidebar, 
            text="Software FJ", 
            font=("Helvetica", 20, "bold"), 
            bg=self.sidebar_color, 
            fg=self.text_light
        )
        label_titulo.pack(pady=(35, 5), padx=10)

        label_subtitulo = tk.Label(
            self.sidebar, 
            text="Gestión de Reservas", 
            font=("Helvetica", 10, "italic"), 
            bg=self.sidebar_color, 
            fg="#94A3B8"
        )
        label_subtitulo.pack(pady=(0, 35))

        # Botones de navegación
        self.btn_clientes = self.crear_boton_navegacion("Clientes", lambda: self.mostrar_vista("clientes"))
        self.btn_servicios = self.crear_boton_navegacion("Servicios", lambda: self.mostrar_vista("servicios"))
        self.btn_reservas = self.crear_boton_navegacion("Reservas", lambda: self.mostrar_vista("reservas"))
        self.btn_logs = self.crear_boton_navegacion("Logs y Simulación", lambda: self.mostrar_vista("logs"))

    def crear_boton_navegacion(self, texto, comando):
        """Crea un botón de navegación estilizado para el sidebar."""
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
            cursor="hand2"
        )
        btn.pack(fill="x", pady=3)
        
        # Efectos visuales de hover
        btn.bind("<Enter>", lambda e: btn.configure(bg="#334155") if self.vista_actual_nombre != texto.lower().split()[0] else None)
        btn.bind("<Leave>", lambda e: btn.configure(bg=self.sidebar_color) if self.vista_actual_nombre != texto.lower().split()[0] else None)
        return btn

    def crear_contenedor_principal(self):
        """Contenedor en la parte derecha donde se renderizarán las vistas dinámicamente."""
        self.contenedor = tk.Frame(self.root, bg=self.bg_color)
        self.contenedor.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.contenedor.grid_columnconfigure(0, weight=1)
        self.contenedor.grid_rowconfigure(0, weight=1)

    def mostrar_vista(self, nombre_vista):
        """Alterna el panel principal con la vista seleccionada."""
        self.vista_actual_nombre = nombre_vista

        # Limpiar selección visual en los botones
        self.btn_clientes.configure(bg=self.sidebar_color)
        self.btn_servicios.configure(bg=self.sidebar_color)
        self.btn_reservas.configure(bg=self.sidebar_color)
        self.btn_logs.configure(bg=self.sidebar_color)

        # Retirar vista actual si existe
        if self.vista_actual:
            self.vista_actual.pack_forget()

        # Cargar y resaltar botón correspondiente
        if nombre_vista == "clientes":
            self.btn_clientes.configure(bg=self.accent_color)
            self.vista_actual = self.obtener_o_crear_vista_clientes()
        elif nombre_vista == "servicios":
            self.btn_servicios.configure(bg=self.accent_color)
            self.vista_actual = self.obtener_o_crear_vista_servicios()
        elif nombre_vista == "reservas":
            self.btn_reservas.configure(bg=self.accent_color)
            self.vista_actual = self.obtener_o_crear_vista_reservas()
        elif nombre_vista == "logs":
            self.btn_logs.configure(bg=self.accent_color)
            self.vista_actual = self.obtener_o_crear_vista_logs()

        self.vista_actual.pack(fill="both", expand=True)

    # Pestañas temporales/placeholders a reemplazar en los hitos 8 y 9
    def obtener_o_crear_vista_clientes(self):
        if "clientes" not in self.vistas:
            frame = tk.Frame(self.contenedor, bg=self.bg_color)
            lbl = tk.Label(
                frame, 
                text="Módulo de Clientes\n\n(En desarrollo - Hito 8)", 
                font=("Helvetica", 16, "bold"), 
                bg=self.bg_color, 
                fg=self.text_dark
            )
            lbl.pack(pady=150)
            self.vistas["clientes"] = frame
        return self.vistas["clientes"]

    def obtener_o_crear_vista_servicios(self):
        if "servicios" not in self.vistas:
            frame = tk.Frame(self.contenedor, bg=self.bg_color)
            lbl = tk.Label(
                frame, 
                text="Módulo de Servicios\n\n(En desarrollo - Hito 8)", 
                font=("Helvetica", 16, "bold"), 
                bg=self.bg_color, 
                fg=self.text_dark
            )
            lbl.pack(pady=150)
            self.vistas["servicios"] = frame
        return self.vistas["servicios"]

    def obtener_o_crear_vista_reservas(self):
        if "reservas" not in self.vistas:
            frame = tk.Frame(self.contenedor, bg=self.bg_color)
            lbl = tk.Label(
                frame, 
                text="Módulo de Reservas\n\n(En desarrollo - Hito 9)", 
                font=("Helvetica", 16, "bold"), 
                bg=self.bg_color, 
                fg=self.text_dark
            )
            lbl.pack(pady=150)
            self.vistas["reservas"] = frame
        return self.vistas["reservas"]

    def obtener_o_crear_vista_logs(self):
        if "logs" not in self.vistas:
            frame = tk.Frame(self.contenedor, bg=self.bg_color)
            lbl = tk.Label(
                frame, 
                text="Módulo de Logs y Simulación\n\n(En desarrollo - Hito 9)", 
                font=("Helvetica", 16, "bold"), 
                bg=self.bg_color, 
                fg=self.text_dark
            )
            lbl.pack(pady=150)
            self.vistas["logs"] = frame
        return self.vistas["logs"]

def iniciar_app():
    root = tk.Tk()
    app = ApplicationGUI(root)
    root.mainloop()
