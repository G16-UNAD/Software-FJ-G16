from src.servicios.base import Servicio
from src.exceptions import ServicioInvalidoError, CalculoCostoError

class ReservaSala(Servicio):
    """
    Servicio de Reserva de Sala.
    Hereda de Servicio e implementa el cálculo de costos sobrecargado.
    """
    def __init__(self, tipo_sala, capacidad, horas, costo_base_por_hora, id_entidad=None):
        super().__init__("Reserva de Sala", costo_base_por_hora, id_entidad)
        self.tipo_sala = tipo_sala
        self.capacidad = capacidad
        self.horas = horas
        self.validar_parametros()

    def validar_parametros(self):
        if not self.tipo_sala or not isinstance(self.tipo_sala, str):
            raise ServicioInvalidoError("El tipo de sala debe ser un texto no vacío.")
        if not isinstance(self.capacidad, int) or self.capacidad <= 0:
            raise ServicioInvalidoError("La capacidad de la sala debe ser un número entero positivo.")
        if not isinstance(self.horas, int) or self.horas <= 0:
            raise ServicioInvalidoError("Las horas reservadas deben ser un número entero positivo.")

    def calcular_costo(self, descuento=0.0, impuesto=0.0, **kwargs) -> float:
        """
        Sobrecarga de cálculo de costo:
        Costo = (costo_base * horas) - descuento + ((costo_base * horas - descuento) * impuesto)
        """
        if descuento < 0:
            raise CalculoCostoError("El descuento no puede ser un valor negativo.")
        if impuesto < 0:
            raise CalculoCostoError("El porcentaje de impuesto no puede ser negativo.")
        
        costo_bruto = self.costo_base * self.horas
        if descuento > costo_bruto:
            raise CalculoCostoError(f"El descuento (${descuento}) supera el costo bruto del servicio (${costo_bruto}).")
        
        costo_neto = costo_bruto - descuento
        costo_total = costo_neto + (costo_neto * impuesto)
        return costo_total

    def obtener_descripcion(self) -> str:
        return f"Sala tipo '{self.tipo_sala}' con capacidad para {self.capacidad} personas por un total de {self.horas} horas."
