class SoftwareFJException(Exception):
    """Excepción base para todos los errores de la aplicación Software FJ."""
    pass

class ClienteInvalidoError(SoftwareFJException):
    """Excepción lanzada cuando los datos de un cliente no son válidos."""
    pass

class ServicioInvalidoError(SoftwareFJException):
    """Excepción lanzada cuando la parametrización de un servicio no cumple con los requisitos."""
    pass

class ReservaInvalidaError(SoftwareFJException):
    """Excepción lanzada por errores de flujo, estado o datos en las reservas."""
    pass

class CalculoCostoError(SoftwareFJException):
    """Excepción lanzada cuando hay inconsistencias matemáticas en el cálculo de costos."""
    pass
