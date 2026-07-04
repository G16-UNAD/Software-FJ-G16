# src/gui/v_logs.py
import tkinter as tk
from tkinter import ttk, messagebox
import os
import threading
from src.logger import logger


class LogsView(tk.Frame):
    """Vista de Logs y Simulación.

    Muestra el contenido del archivo ``app.log`` en un área de texto de solo
    lectura y proporciona un botón para ejecutar la simulación completa de
    las 10 operaciones definidas en ``main.ejecutar_simulacion()``.
    """

    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg_color)
        self.controller = controller
        self.log_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "app.log",
        )

        # Título
        tk.Label(
            self,
            text="Consola de Logs y Simulación",
            font=("Helvetica", 18, "bold"),
            bg=controller.bg_color,
            fg=controller.text_dark,
        ).pack(anchor="w", pady=(0, 15))

        # Barra de acciones
        frame_acciones = tk.Frame(self, bg=controller.bg_color)
        frame_acciones.pack(fill="x", pady=(0, 10))

        btn_simulacion = tk.Button(
            frame_acciones,
            text="▶ Ejecutar Simulación (10 Operaciones)",
            command=self.ejecutar_simulacion,
            font=("Helvetica", 10, "bold"),
            bg="#16A34A",
            fg=controller.text_light,
            activebackground="#15803D",
            activeforeground=controller.text_light,
            bd=0,
            height=2,
            padx=15,
            cursor="hand2",
        )
        btn_simulacion.pack(side="left", padx=(0, 10))

        btn_refrescar = tk.Button(
            frame_acciones,
            text="🔄 Refrescar Logs",
            command=self.cargar_logs,
            font=("Helvetica", 10, "bold"),
            bg=controller.accent_color,
            fg=controller.text_light,
            activebackground="#2563EB",
            activeforeground=controller.text_light,
            bd=0,
            height=2,
            padx=15,
            cursor="hand2",
        )
        btn_refrescar.pack(side="left", padx=(0, 10))

        btn_limpiar = tk.Button(
            frame_acciones,
            text="🗑 Limpiar Log",
            command=self.limpiar_log,
            font=("Helvetica", 10, "bold"),
            bg="#DC2626",
            fg=controller.text_light,
            activebackground="#B91C1C",
            activeforeground=controller.text_light,
            bd=0,
            height=2,
            padx=15,
            cursor="hand2",
        )
        btn_limpiar.pack(side="left")

        frame_log = tk.LabelFrame(
            self,
            text="Registro de Eventos (app.log)",
            font=("Helvetica", 11, "bold"),
            bg=controller.bg_color,
            fg=controller.text_dark,
            padx=10,
            pady=10,
        )
        frame_log.pack(fill="both", expand=True)

        scroll_y = ttk.Scrollbar(frame_log, orient="vertical")
        scroll_y.pack(side="right", fill="y")

        scroll_x = ttk.Scrollbar(frame_log, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")

        self.text_logs = tk.Text(
            frame_log,
            wrap="none",
            font=("Consolas", 9),
            bg="#0F172A",
            fg="#E2E8F0",
            insertbackground="#E2E8F0",
            state="disabled",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
        )
        self.text_logs.pack(fill="both", expand=True)
        scroll_y.config(command=self.text_logs.yview)
        scroll_x.config(command=self.text_logs.xview)

        self.cargar_logs()

    # ------------------------------------------------------------------
    # Cargar contenido del archivo de log
    # ------------------------------------------------------------------
    def cargar_logs(self):
        """Lee el archivo app.log y lo muestra en el área de texto."""
        self.text_logs.config(state="normal")
        self.text_logs.delete("1.0", tk.END)

        try:
            if os.path.exists(self.log_path):
                with open(self.log_path, "r", encoding="utf-8") as f:
                    contenido = f.read()
                self.text_logs.insert(tk.END, contenido)
            else:
                self.text_logs.insert(tk.END, "[INFO] El archivo app.log aún no existe.\n")
        except Exception as e:
            self.text_logs.insert(tk.END, f"[ERROR] No se pudo leer app.log: {e}\n")

        self.text_logs.config(state="disabled")
        self.text_logs.see(tk.END)

    # ------------------------------------------------------------------
    # Ejecutar la simulación de 10 operaciones
    # ------------------------------------------------------------------
    def ejecutar_simulacion(self):
        """Ejecuta la simulación de consola en un hilo separado para no
        bloquear la interfaz gráfica, y luego refresca los logs."""
        try:
            from main import ejecutar_simulacion as sim

            logger.info("Simulación lanzada desde la interfaz gráfica.")
            def _run():
                try:
                    sim()
                except Exception as e:
                    logger.error(f"Error durante la simulación: {e}")
                finally:
                    self.after(500, self.cargar_logs)

            hilo = threading.Thread(target=_run, daemon=True)
            hilo.start()
            messagebox.showinfo(
                "Simulación Iniciada",
                "La simulación de 10 operaciones ha comenzado.\n"
                "Los resultados aparecerán en el panel de logs en unos segundos.",
            )
        except ImportError as e:
            logger.error(f"No se pudo importar la función de simulación: {e}")
            messagebox.showerror("Error de Importación", f"No se encontró la función de simulación: {e}")
        except Exception as e:
            logger.error(f"Error inesperado al ejecutar la simulación: {e}")
            messagebox.showerror("Error Inesperado", f"{e}")

    # ------------------------------------------------------------------
    # Limpiar el archivo de log
    # ------------------------------------------------------------------
    def limpiar_log(self):
        """Vacía el contenido del archivo app.log y refresca la vista."""
        respuesta = messagebox.askyesno(
            "Confirmar limpieza",
            "¿Desea borrar todo el contenido del archivo app.log?",
        )
        if respuesta:
            try:
                with open(self.log_path, "w", encoding="utf-8") as f:
                    f.write("")
                logger.info("Archivo app.log limpiado desde la GUI.")
                self.cargar_logs()
            except Exception as e:
                logger.error(f"Error al limpiar app.log: {e}")
                messagebox.showerror("Error", f"No se pudo limpiar el archivo: {e}")
