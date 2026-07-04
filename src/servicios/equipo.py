from src.servicios.base import Servicio
from src.exceptions import ServicioInvalidoError, CalculoCostoError

class AlquilerEquipos(Servicio):
    """
    Servicio de Alquiler de Equipos.
    Hereda de Servicio e implementa el cálculo de costos sobrecargado.
    """
    def __init__(self, equipo, cantidad, dias, costo_por_dia, id_entidad=None):
        super().__init__("Alquiler de Equipos", costo_por_dia, id_entidad)
        self.equipo = equipo
        self.cantidad = cantidad
        self.dias = dias
        self.validar_parametros()

    def validar_parametros(self):
        if not self.equipo or not isinstance(self.equipo, str):
            raise ServicioInvalidoError("El nombre del equipo debe ser un texto no vacío.")
        if not isinstance(self.cantidad, int) or self.cantidad <= 0:
            raise ServicioInvalidoError("La cantidad de equipos debe ser un número entero positivo.")
        if not isinstance(self.dias, int) or self.dias <= 0:
            raise ServicioInvalidoError("La cantidad de días de alquiler debe ser un número entero positivo.")

    def calcular_costo(self, descuento_porcentaje=0.0, seguro=0.0, **kwargs) -> float:
        """
        Sobrecarga de cálculo de costo:
        Costo = (costo_base * cantidad * dias) * (1 - descuento_porcentaje) + seguro
        """
        if not (0.0 <= descuento_porcentaje <= 1.0):
            raise CalculoCostoError("El descuento en porcentaje debe estar en el rango de 0.0 a 1.0 (0% a 100%).")
        if seguro < 0:
            raise CalculoCostoError("El valor de seguro no puede ser negativo.")
        
        costo_bruto = self.costo_base * self.cantidad * self.dias
        costo_total = (costo_bruto * (1.0 - descuento_porcentaje)) + seguro
        return costo_total

    def obtener_descripcion(self) -> str:
        return f"Alquiler de {self.cantidad}x '{self.equipo}' durante {self.dias} días."
