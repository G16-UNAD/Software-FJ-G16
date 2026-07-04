from src.servicios.base import Servicio
from src.exceptions import ServicioInvalidoError

class AsesoriaEspecializada(Servicio):
    """
    Servicio de Asesoría Especializada.
    Hereda de Servicio e implementa el cálculo de costos sobrecargado.
    """
    def __init__(self, tema, consultor, horas, tarifa_hora, id_entidad=None):
        super().__init__("Asesoría Especializada", tarifa_hora, id_entidad)
        self.tema = tema
        self.consultor = consultor
        self.horas = horas
        self.validar_parametros()

    def validar_parametros(self):
        if not self.tema or not isinstance(self.tema, str):
            raise ServicioInvalidoError("El tema de la asesoría debe ser un texto no vacío.")
        if not self.consultor or not isinstance(self.consultor, str):
            raise ServicioInvalidoError("El consultor asignado debe ser un texto no vacío.")
        if not isinstance(self.horas, int) or self.horas <= 0:
            raise ServicioInvalidoError("Las horas de asesoría deben ser un número entero positivo.")

    def calcular_costo(self, es_urgente=False, **kwargs) -> float:
        """
        Sobrecarga de cálculo de costo:
        Si la asesoría es de carácter urgente, aplica un recargo del 20% sobre el costo total.
        Costo = tarifa_hora * horas * (1.20 si es_urgente)
        """
        costo_total = self.costo_base * self.horas
        if es_urgente:
            costo_total *= 1.20
        return costo_total

    def obtener_descripcion(self) -> str:
        return f"Asesoría en '{self.tema}' dirigida por el consultor '{self.consultor}' ({self.horas} horas)."
