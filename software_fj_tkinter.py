# ============================================================
# SISTEMA SOFTWARE FJ CON INTERFAZ TKINTER
# Programación Orientada a Objetos + Excepciones + Logs
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
from datetime import datetime


# ============================================================
# ARCHIVO DE LOGS
# ============================================================

LOG_FILE = "software_fj_logs.txt"


def registrar_log(mensaje):
    """
    Registra eventos y errores en un archivo de texto.
    """
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as archivo:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo.write(f"[{fecha}] {mensaje}\n")
    except Exception as e:
        print("No se pudo escribir en el archivo de logs:", e)


# ============================================================
# EXCEPCIONES PERSONALIZADAS
# ============================================================

class ErrorSistema(Exception):
    pass


class ErrorValidacion(ErrorSistema):
    pass


class ErrorServicioNoDisponible(ErrorSistema):
    pass


class ErrorReserva(ErrorSistema):
    pass


class ErrorCalculo(ErrorSistema):
    pass


# ============================================================
# CLASE ABSTRACTA GENERAL
# ============================================================

class EntidadSistema(ABC):
    """
    Clase abstracta base.
    Todas las entidades principales del sistema heredan de esta clase.
    """

    def __init__(self, codigo):
        if not codigo:
            raise ErrorValidacion("El código no puede estar vacío.")
        self._codigo = codigo

    @property
    def codigo(self):
        return self._codigo

    @abstractmethod
    def mostrar_info(self):
        pass


# ============================================================
# CLASE CLIENTE
# ============================================================

class Cliente(EntidadSistema):
    """
    Clase Cliente.
    Aplica encapsulación con atributos privados.
    """

    def __init__(self, codigo, nombre, correo, telefono):
        super().__init__(codigo)

        self.__nombre = None
        self.__correo = None
        self.__telefono = None

        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

        registrar_log(f"Cliente creado: {self.__nombre}")

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or len(valor.strip()) < 3:
            raise ErrorValidacion("El nombre debe tener mínimo 3 caracteres.")
        self.__nombre = valor.strip()

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not valor or "@" not in valor or "." not in valor:
            raise ErrorValidacion("Correo electrónico inválido.")
        self.__correo = valor.strip()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if not str(valor).isdigit() or len(str(valor)) < 7:
            raise ErrorValidacion("El teléfono debe tener mínimo 7 dígitos.")
        self.__telefono = str(valor)

    def mostrar_info(self):
        return f"{self.codigo} - {self.__nombre} - {self.__correo} - {self.__telefono}"


# ============================================================
# CLASE ABSTRACTA SERVICIO
# ============================================================

class Servicio(EntidadSistema):
    """
    Clase abstracta Servicio.
    Las clases hijas deben implementar sus propios métodos.
    """

    def __init__(self, codigo, nombre, precio_base, disponible=True):
        super().__init__(codigo)

        if not nombre:
            raise ErrorValidacion("El nombre del servicio no puede estar vacío.")

        try:
            precio_base = float(precio_base)
        except ValueError as error:
            raise ErrorValidacion("El precio base debe ser numérico.") from error

        if precio_base <= 0:
            raise ErrorValidacion("El precio base debe ser mayor que cero.")

        self._nombre = nombre
        self._precio_base = precio_base
        self._disponible = disponible

    @property
    def nombre(self):
        return self._nombre

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, estado):
        self._disponible = estado

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        pass

    @abstractmethod
    def validar_parametros(self, duracion):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    def mostrar_info(self):
        return self.describir_servicio()


# ============================================================
# SERVICIO 1: RESERVA DE SALA
# ============================================================

class ReservaSala(Servicio):

    def __init__(self, codigo, nombre, precio_base, capacidad):
        super().__init__(codigo, nombre, precio_base)

        try:
            capacidad = int(capacidad)
        except ValueError as error:
            raise ErrorValidacion("La capacidad debe ser numérica.") from error

        if capacidad <= 0:
            raise ErrorValidacion("La capacidad debe ser mayor que cero.")

        self.__capacidad = capacidad

    def validar_parametros(self, duracion):
        if duracion <= 0:
            raise ErrorReserva("La duración debe ser mayor que cero.")
        if duracion > 8:
            raise ErrorReserva("Una sala no puede reservarse por más de 8 horas.")

    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        self.validar_parametros(duracion)

        subtotal = self._precio_base * duracion
        total = subtotal + (subtotal * impuesto) - descuento

        if total < 0:
            raise ErrorCalculo("El total no puede ser negativo.")

        return total

    def describir_servicio(self):
        return f"Sala | {self.codigo} | {self._nombre} | Capacidad: {self.__capacidad} | ${self._precio_base}/hora"


# ============================================================
# SERVICIO 2: ALQUILER DE EQUIPO
# ============================================================

class AlquilerEquipo(Servicio):

    def __init__(self, codigo, nombre, precio_base, tipo_equipo):
        super().__init__(codigo, nombre, precio_base)

        if not tipo_equipo:
            raise ErrorValidacion("El tipo de equipo no puede estar vacío.")

        self.__tipo_equipo = tipo_equipo

    def validar_parametros(self, duracion):
        if duracion <= 0:
            raise ErrorReserva("La duración debe ser mayor que cero.")
        if duracion > 30:
            raise ErrorReserva("Un equipo no puede alquilarse por más de 30 días.")

    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        self.validar_parametros(duracion)

        subtotal = self._precio_base * duracion

        if duracion >= 7:
            subtotal *= 0.90

        total = subtotal + (subtotal * impuesto) - descuento

        if total < 0:
            raise ErrorCalculo("El total no puede ser negativo.")

        return total

    def describir_servicio(self):
        return f"Equipo | {self.codigo} | {self._nombre} | Tipo: {self.__tipo_equipo} | ${self._precio_base}/día"


# ============================================================
# SERVICIO 3: ASESORÍA ESPECIALIZADA
# ============================================================

class AsesoriaEspecializada(Servicio):

    def __init__(self, codigo, nombre, precio_base, especialista):
        super().__init__(codigo, nombre, precio_base)

        if not especialista:
            raise ErrorValidacion("El especialista no puede estar vacío.")

        self.__especialista = especialista

    def validar_parametros(self, duracion):
        if duracion <= 0:
            raise ErrorReserva("La duración debe ser mayor que cero.")
        if duracion > 5:
            raise ErrorReserva("Una asesoría no puede durar más de 5 horas.")

    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        self.validar_parametros(duracion)

        subtotal = self._precio_base * duracion
        recargo = 50
        total = subtotal + recargo + (subtotal * impuesto) - descuento

        if total < 0:
            raise ErrorCalculo("El total no puede ser negativo.")

        return total

    def describir_servicio(self):
        return f"Asesoría | {self.codigo} | {self._nombre} | Especialista: {self.__especialista} | ${self._precio_base}/hora"


# ============================================================
# CLASE RESERVA
# ============================================================

class Reserva:
    """
    Clase que relaciona un cliente con un servicio.
    """

    contador = 1

    def __init__(self, cliente, servicio, duracion):
        if not isinstance(cliente, Cliente):
            raise ErrorReserva("Cliente inválido.")

        if not isinstance(servicio, Servicio):
            raise ErrorReserva("Servicio inválido.")

        if not servicio.disponible:
            raise ErrorServicioNoDisponible("El servicio no está disponible.")

        try:
            duracion = float(duracion)
        except ValueError as error:
            raise ErrorValidacion("La duración debe ser numérica.") from error

        servicio.validar_parametros(duracion)

        self.codigo = f"R{Reserva.contador:03d}"
        Reserva.contador += 1

        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = "Pendiente"

        registrar_log(f"Reserva creada: {self.codigo}")

    @property
    def estado(self):
        return self.__estado

    def confirmar(self):
        if self.__estado != "Pendiente":
            raise ErrorReserva("Solo se pueden confirmar reservas pendientes.")
        self.__estado = "Confirmada"
        registrar_log(f"Reserva confirmada: {self.codigo}")

    def cancelar(self):
        if self.__estado == "Cancelada":
            raise ErrorReserva("La reserva ya estaba cancelada.")
        self.__estado = "Cancelada"
        registrar_log(f"Reserva cancelada: {self.codigo}")

    def procesar(self):
        """
        Uso de try/except/else/finally.
        """
        try:
            if self.__estado != "Confirmada":
                raise ErrorReserva("La reserva debe estar confirmada antes de procesarse.")

            costo = self.__servicio.calcular_costo(
                self.__duracion,
                impuesto=0.10,
                descuento=5
            )

        except ErrorSistema as e:
            registrar_log(f"Error procesando reserva {self.codigo}: {e}")
            raise

        else:
            self.__estado = "Procesada"
            registrar_log(f"Reserva procesada: {self.codigo} | Costo: ${costo:.2f}")
            return costo

        finally:
            registrar_log(f"Finalizó intento de procesamiento de reserva {self.codigo}")

    def mostrar_info(self):
        return f"{self.codigo} | Cliente: {self.__cliente.nombre} | Servicio: {self.__servicio.nombre} | Duración: {self.__duracion} | Estado: {self.__estado}"


# ============================================================
# CLASE SISTEMA PRINCIPAL
# ============================================================

class SistemaSoftwareFJ:
    """
    Clase central del sistema.
    Maneja listas internas de clientes, servicios y reservas.
    """

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []
        registrar_log("Sistema Software FJ iniciado.")

    def agregar_cliente(self, cliente):
        self.clientes.append(cliente)

    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)

    def agregar_reserva(self, reserva):
        self.reservas.append(reserva)


# ============================================================
# INTERFAZ GRÁFICA CON TKINTER
# ============================================================

class AplicacionSoftwareFJ:
    """
    Clase de la interfaz gráfica.
    También es parte de la arquitectura orientada a objetos.
    """

    def __init__(self, ventana):
        self.sistema = SistemaSoftwareFJ()
        self.ventana = ventana

        self.ventana.title("Software FJ - Sistema de Reservas")
        self.ventana.geometry("950x650")

        self.crear_interfaz()

    def crear_interfaz(self):
        """
        Construye todos los elementos visuales.
        """

        titulo = tk.Label(
            self.ventana,
            text="SOFTWARE FJ - Gestión de Clientes, Servicios y Reservas",
            font=("Arial", 16, "bold")
        )
        titulo.pack(pady=10)

        panel = ttk.Notebook(self.ventana)
        panel.pack(expand=True, fill="both")

        self.tab_clientes = ttk.Frame(panel)
        self.tab_servicios = ttk.Frame(panel)
        self.tab_reservas = ttk.Frame(panel)
        self.tab_simulacion = ttk.Frame(panel)

        panel.add(self.tab_clientes, text="Clientes")
        panel.add(self.tab_servicios, text="Servicios")
        panel.add(self.tab_reservas, text="Reservas")
        panel.add(self.tab_simulacion, text="Simulación")

        self.crear_tab_clientes()
        self.crear_tab_servicios()
        self.crear_tab_reservas()
        self.crear_tab_simulacion()

    # ========================================================
    # PESTAÑA CLIENTES
    # ========================================================

    def crear_tab_clientes(self):
        frame = self.tab_clientes

        tk.Label(frame, text="Código").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(frame, text="Nombre").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(frame, text="Correo").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(frame, text="Teléfono").grid(row=3, column=0, padx=5, pady=5)

        self.codigo_cliente = tk.Entry(frame)
        self.nombre_cliente = tk.Entry(frame)
        self.correo_cliente = tk.Entry(frame)
        self.telefono_cliente = tk.Entry(frame)

        self.codigo_cliente.grid(row=0, column=1)
        self.nombre_cliente.grid(row=1, column=1)
        self.correo_cliente.grid(row=2, column=1)
        self.telefono_cliente.grid(row=3, column=1)

        tk.Button(frame, text="Registrar Cliente", command=self.registrar_cliente).grid(row=4, column=0, columnspan=2, pady=10)

        self.lista_clientes = tk.Listbox(frame, width=100)
        self.lista_clientes.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    def registrar_cliente(self):
        try:
            cliente = Cliente(
                self.codigo_cliente.get(),
                self.nombre_cliente.get(),
                self.correo_cliente.get(),
                self.telefono_cliente.get()
            )

        except ErrorSistema as e:
            registrar_log(f"Error registrando cliente desde interfaz: {e}")
            messagebox.showerror("Error de validación", str(e))

        except Exception as e:
            registrar_log(f"Error inesperado registrando cliente: {e}")
            messagebox.showerror("Error inesperado", str(e))

        else:
            self.sistema.agregar_cliente(cliente)
            self.actualizar_clientes()
            messagebox.showinfo("Éxito", "Cliente registrado correctamente.")

        finally:
            registrar_log("Finalizó intento de registro de cliente.")

    # ========================================================
    # PESTAÑA SERVICIOS
    # ========================================================

    def crear_tab_servicios(self):
        frame = self.tab_servicios

        tk.Label(frame, text="Tipo de servicio").grid(row=0, column=0, padx=5, pady=5)

        self.tipo_servicio = ttk.Combobox(frame, values=["Sala", "Equipo", "Asesoría"])
        self.tipo_servicio.grid(row=0, column=1)
        self.tipo_servicio.current(0)

        tk.Label(frame, text="Código").grid(row=1, column=0)
        tk.Label(frame, text="Nombre").grid(row=2, column=0)
        tk.Label(frame, text="Precio base").grid(row=3, column=0)
        tk.Label(frame, text="Dato extra").grid(row=4, column=0)

        self.codigo_servicio = tk.Entry(frame)
        self.nombre_servicio = tk.Entry(frame)
        self.precio_servicio = tk.Entry(frame)
        self.extra_servicio = tk.Entry(frame)

        self.codigo_servicio.grid(row=1, column=1)
        self.nombre_servicio.grid(row=2, column=1)
        self.precio_servicio.grid(row=3, column=1)
        self.extra_servicio.grid(row=4, column=1)

        tk.Label(
            frame,
            text="Dato extra: capacidad para sala, tipo de equipo o nombre del especialista."
        ).grid(row=5, column=0, columnspan=2, pady=5)

        tk.Button(frame, text="Crear Servicio", command=self.crear_servicio).grid(row=6, column=0, columnspan=2, pady=10)

        self.lista_servicios = tk.Listbox(frame, width=120)
        self.lista_servicios.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

    def crear_servicio(self):
        try:
            tipo = self.tipo_servicio.get()

            if tipo == "Sala":
                servicio = ReservaSala(
                    self.codigo_servicio.get(),
                    self.nombre_servicio.get(),
                    self.precio_servicio.get(),
                    self.extra_servicio.get()
                )

            elif tipo == "Equipo":
                servicio = AlquilerEquipo(
                    self.codigo_servicio.get(),
                    self.nombre_servicio.get(),
                    self.precio_servicio.get(),
                    self.extra_servicio.get()
                )

            elif tipo == "Asesoría":
                servicio = AsesoriaEspecializada(
                    self.codigo_servicio.get(),
                    self.nombre_servicio.get(),
                    self.precio_servicio.get(),
                    self.extra_servicio.get()
                )

            else:
                raise ErrorValidacion("Tipo de servicio no válido.")

        except ErrorSistema as e:
            registrar_log(f"Error creando servicio desde interfaz: {e}")
            messagebox.showerror("Error de servicio", str(e))

        except Exception as e:
            registrar_log(f"Error inesperado creando servicio: {e}")
            messagebox.showerror("Error inesperado", str(e))

        else:
            self.sistema.agregar_servicio(servicio)
            self.actualizar_servicios()
            self.actualizar_combos()
            messagebox.showinfo("Éxito", "Servicio creado correctamente.")

        finally:
            registrar_log("Finalizó intento de creación de servicio.")

    # ========================================================
    # PESTAÑA RESERVAS
    # ========================================================

    def crear_tab_reservas(self):
        frame = self.tab_reservas

        tk.Label(frame, text="Cliente").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(frame, text="Servicio").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(frame, text="Duración").grid(row=2, column=0, padx=5, pady=5)

        self.combo_clientes = ttk.Combobox(frame, width=50)
        self.combo_servicios = ttk.Combobox(frame, width=70)
        self.duracion_reserva = tk.Entry(frame)

        self.combo_clientes.grid(row=0, column=1)
        self.combo_servicios.grid(row=1, column=1)
        self.duracion_reserva.grid(row=2, column=1)

        tk.Button(frame, text="Crear Reserva", command=self.crear_reserva).grid(row=3, column=0, pady=10)
        tk.Button(frame, text="Confirmar Reserva", command=self.confirmar_reserva).grid(row=3, column=1, pady=10)
        tk.Button(frame, text="Procesar Reserva", command=self.procesar_reserva).grid(row=3, column=2, pady=10)
        tk.Button(frame, text="Cancelar Reserva", command=self.cancelar_reserva).grid(row=3, column=3, pady=10)

        self.lista_reservas = tk.Listbox(frame, width=130)
        self.lista_reservas.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

    def crear_reserva(self):
        try:
            indice_cliente = self.combo_clientes.current()
            indice_servicio = self.combo_servicios.current()

            if indice_cliente == -1:
                raise ErrorReserva("Debe seleccionar un cliente.")

            if indice_servicio == -1:
                raise ErrorReserva("Debe seleccionar un servicio.")

            cliente = self.sistema.clientes[indice_cliente]
            servicio = self.sistema.servicios[indice_servicio]

            reserva = Reserva(cliente, servicio, self.duracion_reserva.get())

        except ErrorSistema as e:
            registrar_log(f"Error creando reserva desde interfaz: {e}")
            messagebox.showerror("Error de reserva", str(e))

        except Exception as e:
            registrar_log(f"Error inesperado creando reserva: {e}")
            messagebox.showerror("Error inesperado", str(e))

        else:
            self.sistema.agregar_reserva(reserva)
            self.actualizar_reservas()
            messagebox.showinfo("Éxito", "Reserva creada correctamente.")

        finally:
            registrar_log("Finalizó intento de creación de reserva.")

    def obtener_reserva_seleccionada(self):
        seleccion = self.lista_reservas.curselection()

        if not seleccion:
            raise ErrorReserva("Debe seleccionar una reserva de la lista.")

        return self.sistema.reservas[seleccion[0]]

    def confirmar_reserva(self):
        try:
            reserva = self.obtener_reserva_seleccionada()
            reserva.confirmar()

        except ErrorSistema as e:
            registrar_log(f"Error confirmando reserva: {e}")
            messagebox.showerror("Error", str(e))

        else:
            self.actualizar_reservas()
            messagebox.showinfo("Éxito", "Reserva confirmada.")

    def procesar_reserva(self):
        try:
            reserva = self.obtener_reserva_seleccionada()
            costo = reserva.procesar()

        except ErrorSistema as e:
            registrar_log(f"Error procesando reserva: {e}")
            messagebox.showerror("Error", str(e))

        else:
            self.actualizar_reservas()
            messagebox.showinfo("Reserva procesada", f"Costo final: ${costo:.2f}")

    def cancelar_reserva(self):
        try:
            reserva = self.obtener_reserva_seleccionada()
            reserva.cancelar()

        except ErrorSistema as e:
            registrar_log(f"Error cancelando reserva: {e}")
            messagebox.showerror("Error", str(e))

        else:
            self.actualizar_reservas()
            messagebox.showinfo("Éxito", "Reserva cancelada.")

    # ========================================================
    # PESTAÑA SIMULACIÓN
    # ========================================================

    def crear_tab_simulacion(self):
        frame = self.tab_simulacion

        tk.Label(
            frame,
            text="Simulación automática de operaciones válidas e inválidas",
            font=("Arial", 13, "bold")
        ).pack(pady=10)

        tk.Button(
            frame,
            text="Ejecutar 10 operaciones de prueba",
            command=self.ejecutar_simulacion
        ).pack(pady=10)

        self.resultado_simulacion = tk.Text(frame, width=110, height=25)
        self.resultado_simulacion.pack(padx=10, pady=10)

    def escribir_simulacion(self, texto):
        self.resultado_simulacion.insert(tk.END, texto + "\n")
        self.resultado_simulacion.see(tk.END)

    def ejecutar_simulacion(self):
        self.resultado_simulacion.delete("1.0", tk.END)

        operaciones = [
            "1. Crear cliente válido",
            "2. Crear cliente inválido",
            "3. Crear sala válida",
            "4. Crear equipo válido",
            "5. Crear asesoría válida",
            "6. Crear servicio inválido",
            "7. Crear reserva exitosa",
            "8. Crear reserva con duración inválida",
            "9. Servicio no disponible",
            "10. Procesar reserva sin confirmar"
        ]

        for op in operaciones:
            self.escribir_simulacion(op)

        try:
            cliente = Cliente("C100", "Carlos Torres", "carlos@email.com", "3004567890")
            self.sistema.agregar_cliente(cliente)
            self.escribir_simulacion("Cliente válido creado correctamente.")
        except Exception as e:
            self.escribir_simulacion(f"Error: {e}")

        try:
            Cliente("C101", "Lu", "correo_malo", "12")
        except Exception as e:
            registrar_log(f"Simulación cliente inválido: {e}")
            self.escribir_simulacion(f"Cliente inválido controlado: {e}")

        try:
            sala = ReservaSala("S100", "Sala Premium", 50, 25)
            equipo = AlquilerEquipo("E100", "Laptop Lenovo", 30, "Computador")
            asesoria = AsesoriaEspecializada("A100", "Asesoría en IA", 100, "Dra. Martínez")

            self.sistema.agregar_servicio(sala)
            self.sistema.agregar_servicio(equipo)
            self.sistema.agregar_servicio(asesoria)

            self.escribir_simulacion("Tres servicios válidos creados correctamente.")

        except Exception as e:
            self.escribir_simulacion(f"Error creando servicios: {e}")

        try:
            ReservaSala("S200", "Sala Mala", -20, 0)
        except Exception as e:
            registrar_log(f"Simulación servicio inválido: {e}")
            self.escribir_simulacion(f"Servicio inválido controlado: {e}")

        try:
            reserva = Reserva(cliente, sala, 3)
            reserva.confirmar()
            costo = reserva.procesar()
            self.sistema.agregar_reserva(reserva)
            self.escribir_simulacion(f"Reserva exitosa procesada. Costo: ${costo:.2f}")
        except Exception as e:
            self.escribir_simulacion(f"Error en reserva exitosa: {e}")

        try:
            Reserva(cliente, sala, 15)
        except Exception as e:
            registrar_log(f"Simulación reserva inválida: {e}")
            self.escribir_simulacion(f"Reserva inválida controlada: {e}")

        try:
            equipo.cambiar_disponibilidad(False)
            Reserva(cliente, equipo, 2)
        except Exception as e:
            registrar_log(f"Simulación servicio no disponible: {e}")
            self.escribir_simulacion(f"Servicio no disponible controlado: {e}")
        finally:
            equipo.cambiar_disponibilidad(True)

        try:
            reserva_sin_confirmar = Reserva(cliente, asesoria, 2)
            self.sistema.agregar_reserva(reserva_sin_confirmar)
            reserva_sin_confirmar.procesar()
        except Exception as e:
            registrar_log(f"Simulación procesar sin confirmar: {e}")
            self.escribir_simulacion(f"Procesamiento inválido controlado: {e}")

        self.actualizar_clientes()
        self.actualizar_servicios()
        self.actualizar_reservas()
        self.actualizar_combos()

        self.escribir_simulacion("\nEl programa terminó la simulación sin detenerse.")
        self.escribir_simulacion(f"Los eventos y errores fueron registrados en: {LOG_FILE}")

    # ========================================================
    # MÉTODOS PARA ACTUALIZAR LISTAS VISUALES
    # ========================================================

    def actualizar_clientes(self):
        self.lista_clientes.delete(0, tk.END)

        for cliente in self.sistema.clientes:
            self.lista_clientes.insert(tk.END, cliente.mostrar_info())

        self.actualizar_combos()

    def actualizar_servicios(self):
        self.lista_servicios.delete(0, tk.END)

        for servicio in self.sistema.servicios:
            self.lista_servicios.insert(tk.END, servicio.mostrar_info())

        self.actualizar_combos()

    def actualizar_reservas(self):
        self.lista_reservas.delete(0, tk.END)

        for reserva in self.sistema.reservas:
            self.lista_reservas.insert(tk.END, reserva.mostrar_info())

    def actualizar_combos(self):
        self.combo_clientes["values"] = [
            cliente.mostrar_info() for cliente in self.sistema.clientes
        ]

        self.combo_servicios["values"] = [
            servicio.mostrar_info() for servicio in self.sistema.servicios
        ]


# ============================================================
# EJECUCIÓN PRINCIPAL
# ============================================================

if __name__ == "__main__":
    ventana = tk.Tk()
    app = AplicacionSoftwareFJ(ventana)
    ventana.mainloop()