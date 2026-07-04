from abc import abstractmethod
from src.base import EntidadBase

class Servicio(EntidadBase):
    """
    Clase abstracta Servicio que hereda de EntidadBase.
    Sirve como base para todos los servicios de Software FJ.
    """
    def __init__(self, nombre_servicio, costo_base, id_entidad=None):
        super().__init__(id_entidad)
        self._nombre_servicio = nombre_servicio
        self.costo_base = costo_base

    @property
    def nombre_servicio(self):
        """Nombre general de la categoría del servicio."""
        return self._nombre_servicio

    @property
    def costo_base(self):
        """Costo base del servicio (debe ser positivo)."""
        return self._costo_base

    @costo_base.setter
    def costo_base(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("El costo base no puede ser negativo ni de un tipo no numérico.")
        self._costo_base = float(value)

    @abstractmethod
    def calcular_costo(self, **kwargs) -> float:
        """
        Calcula el costo del servicio.
        Permite sobrecarga de métodos mediante parámetros opcionales (descuentos, impuestos, etc.).
        """
        pass

    @abstractmethod
    def obtener_descripcion(self) -> str:
        """Retorna una descripción específica de los parámetros del servicio."""
        pass

    @abstractmethod
    def validar_parametros(self):
        """Valida que los atributos y parámetros del servicio sean consistentes."""
        pass

    def obtener_detalles(self) -> str:
        return f"Servicio: {self.nombre_servicio} | Costo Base: ${self.costo_base:.2f}"
