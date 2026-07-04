import re
from src.base import EntidadBase
from src.exceptions import ClienteInvalidoError

class Cliente(EntidadBase):
    """
    Clase Cliente que hereda de EntidadBase.
    Implementa encapsulamiento completo y validaciones para los datos personales.
    """
    def __init__(self, nombre, email, telefono, identificacion, id_entidad=None):
        super().__init__(id_entidad)
        # Usamos los setters para asegurar que las validaciones se apliquen en la creación
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.identificacion = identificacion

    @property
    def nombre(self):
        """Nombre del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        if not value or not isinstance(value, str) or len(value.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")
        self._nombre = value.strip()

    @property
    def email(self):
        """Correo electrónico del cliente (valida formato básico)."""
        return self._email

    @email.setter
    def email(self, value):
        if not value or not isinstance(value, str) or not re.match(r"^[^@]+@[^@]+\.[^@]+$", value.strip()):
            raise ClienteInvalidoError(f"El correo electrónico '{value}' no tiene un formato válido.")
        self._email = value.strip()

    @property
    def telefono(self):
        """Teléfono del cliente (solo dígitos y mínimo 7 caracteres)."""
        return self._telefono

    @telefono.setter
    def telefono(self, value):
        if not value or not isinstance(value, str) or not value.strip().isdigit() or len(value.strip()) < 7:
            raise ClienteInvalidoError("El teléfono debe contener solo dígitos y tener al menos 7 caracteres.")
        self._telefono = value.strip()

    @property
    def identificacion(self):
        """Identificación (cédula o NIT) del cliente."""
        return self._identificacion

    @identificacion.setter
    def identificacion(self, value):
        if not value or not isinstance(value, str) or len(value.strip()) < 5:
            raise ClienteInvalidoError("La identificación debe tener al menos 5 caracteres.")
        self._identificacion = value.strip()

    def obtener_detalles(self) -> str:
        return f"Cliente: {self.nombre} (ID: {self.identificacion}, Email: {self.email}, Tel: {self.telefono})"
