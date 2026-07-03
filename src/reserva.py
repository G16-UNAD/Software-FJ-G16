from src.base import EntidadBase
from src.cliente import Cliente
from src.servicios.base import Servicio
from src.exceptions import ReservaInvalidaError
from src.logger import logger
from datetime import datetime

class Reserva(EntidadBase):
    """
    Clase Reserva que hereda de EntidadBase.
    Asocia un Cliente y un Servicio con manejo de estados, fechas de reserva
    y control de excepciones para la confirmación de la reserva.
    """
    ESTADOS = ["PENDIENTE", "CONFIRMADA", "CANCELADA"]

    def __init__(self, cliente, servicio, fecha_reserva, id_entidad=None):
        super().__init__(id_entidad)
        self.cliente = cliente
        self.servicio = servicio
        self.fecha_reserva = fecha_reserva
        self._estado = "PENDIENTE"
        self._costo_final = 0.0
        self.validar_parametros()
        logger.info(f"Reserva {self.id} creada en estado PENDIENTE para el cliente '{self.cliente.nombre}'.")

    def validar_parametros(self):
        if not isinstance(self.cliente, Cliente):
            raise ReservaInvalidaError("El cliente asignado debe ser una instancia válida de la clase Cliente.")
        if not isinstance(self.servicio, Servicio):
            raise ReservaInvalidaError("El servicio asignado debe ser una instancia válida de la clase Servicio.")
        if not isinstance(self.fecha_reserva, datetime):
            raise ReservaInvalidaError("La fecha de reserva debe ser un objeto de tipo datetime.")
        if self.fecha_reserva < datetime.now():
            raise ReservaInvalidaError("La fecha de reserva no puede estar en el pasado.")

    @property
    def estado(self):
        """Estado actual de la reserva (PENDIENTE, CONFIRMADA, CANCELADA)."""
        return self._estado

    @property
    def costo_final(self):
        """Costo final calculado al confirmar la reserva."""
        return self._costo_final

    def confirmar(self, **opciones_calculo):
        """
        Confirma la reserva y realiza el cálculo de costos usando el método
        calcular_costo() del servicio. Implementa encadenamiento de excepciones.
        """
        if self._estado != "PENDIENTE":
            raise ReservaInvalidaError(f"No se puede confirmar la reserva. Estado actual: '{self._estado}'.")
        
        try:
            # Llama al método sobrecargado del servicio para calcular el costo.
            self._costo_final = self.servicio.calcular_costo(**opciones_calculo)
            self._estado = "CONFIRMADA"
            logger.info(f"Reserva {self.id} CONFIRMADA con éxito. Costo Final: ${self._costo_final:.2f}")
        except Exception as e:
            mensaje = f"Error en la confirmación de la reserva {self.id} debido a una falla en el cálculo de costos."
            logger.error(f"{mensaje} Origen: {e}")
            # Encadenamiento de excepciones
            raise ReservaInvalidaError(mensaje) from e

    def cancelar(self):
        """
        Cancela la reserva.
        """
        if self._estado == "CANCELADA":
            raise ReservaInvalidaError("La reserva ya ha sido CANCELADA previamente.")
        
        self._estado = "CANCELADA"
        logger.info(f"Reserva {self.id} ha sido CANCELADA.")

    def obtener_detalles(self) -> str:
        return (f"Reserva ID: {self.id}\n"
                f"  -> {self.cliente.obtener_detalles()}\n"
                f"  -> {self.servicio.obtener_detalles()}\n"
                f"  -> Detalles del Servicio: {self.servicio.obtener_descripcion()}\n"
                f"  -> Fecha programada: {self.fecha_reserva.strftime('%Y-%m-%d %H:%M')}\n"
                f"  -> Estado actual: {self._estado} | Costo Final Facturado: ${self._costo_final:.2f}")
