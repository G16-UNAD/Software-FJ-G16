from abc import ABC, abstractmethod
import uuid
from datetime import datetime

class EntidadBase(ABC):
    """
    Clase abstracta base para representar entidades generales del sistema.
    Asegura la encapsulación de un identificador único (ID) y la fecha de creación.
    """
    def __init__(self, id_entidad=None):
        self._id = id_entidad if id_entidad else str(uuid.uuid4())
        self._fecha_creacion = datetime.now()

    @property
    def id(self):
        """Identificador único de la entidad (sólo lectura)."""
        return self._id

    @property
    def fecha_creacion(self):
        """Fecha y hora en que se creó la entidad (sólo lectura)."""
        return self._fecha_creacion

    @abstractmethod
    def obtener_detalles(self) -> str:
        """
        Método abstracto para obtener los detalles en texto de la entidad.
        Debe ser implementado por todas las subclases.
        """
        pass
