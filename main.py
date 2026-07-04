import sys
from datetime import datetime, timedelta
from src.logger import logger
from src.exceptions import (
    ClienteInvalidoError,
    ServicioInvalidoError,
    ReservaInvalidaError,
    CalculoCostoError,
    SoftwareFJException
)
from src.cliente import Cliente
from src.servicios.sala import ReservaSala
from src.servicios.equipo import AlquilerEquipos
from src.servicios.asesoria import AsesoriaEspecializada
from src.reserva import Reserva
from src.gui.app import iniciar_app

def ejecutar_simulacion():
    logger.info("======================================================================")
    logger.info("   INICIANDO SIMULACIÓN DE 10 OPERACIONES - SOFTWARE FJ")
    logger.info("======================================================================")

    # Listas en memoria para almacenar las entidades del sistema (simulando una base de datos)
    clientes = []
    servicios = []
    reservas = []

    # -------------------------------------------------------------------------
    # OPERACIÓN 1: Registro de cliente válido
    # -------------------------------------------------------------------------
    logger.info("\n--- OPERACIÓN 1: Registrar Cliente Válido (Juan Pérez) ---")
    try:
        c1 = Cliente("Juan Pérez", "juan.perez@email.com", "3001234567", "10158976")
        clientes.append(c1)
        logger.info(f"ÉXITO: Cliente registrado. {c1.obtener_detalles()}")
    except ClienteInvalidoError as e:
        logger.error(f"FALLO: No se pudo registrar cliente: {e}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 2: Intento de registro de cliente con correo inválido (Fallo controlado)
    # -------------------------------------------------------------------------
    logger.info("\n--- OPERACIÓN 2: Registrar Cliente con Correo Inválido ---")
    try:
        c2 = Cliente("Cristhian Hernandez", "correo-invalido", "3119876543", "80245671")
        clientes.append(c2)
        logger.info(f"ÉXITO: Cliente registrado. {c2.obtener_detalles()}")
    except ClienteInvalidoError as e:
        logger.warning(f"CONTROLADO: Error esperado al crear cliente: {e}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 3: Crear un servicio de Reserva de Sala válido
    # -------------------------------------------------------------------------
    logger.info("\n--- OPERACIÓN 3: Crear Servicio Válido (ReservaSala) ---")
    try:
        # Sala de reuniones, para 10 personas, por 5 horas, costo de $50.0 por hora
        s1 = ReservaSala("Reunión", 10, 5, 50.0)
        servicios.append(s1)
        logger.info(f"ÉXITO: Servicio creado. {s1.obtener_detalles()}")
    except ServicioInvalidoError as e:
        logger.error(f"FALLO: No se pudo crear servicio: {e}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 4: Intento de crear un servicio con parámetros inválidos (Fallo controlado)
    # -------------------------------------------------------------------------
    logger.info("\n--- OPERACIÓN 4: Crear Servicio con Capacidad Negativa ---")
    try:
        # Capacidad inválida de -5 personas
        s2 = ReservaSala("Conferencia", -5, 2, 75.0)
        servicios.append(s2)
        logger.info(f"ÉXITO: Servicio creado. {s2.obtener_detalles()}")
    except ServicioInvalidoError as e:
        logger.warning(f"CONTROLADO: Error esperado al crear servicio: {e}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 5: Crear una Reserva válida en estado PENDIENTE
    # -------------------------------------------------------------------------
    logger.info("\n--- OPERACIÓN 5: Crear Reserva Válida (Estado Pendiente) ---")
    fecha_futura = datetime.now() + timedelta(days=2) # 2 días en el futuro
    reserva_sala = None
    try:
        reserva_sala = Reserva(clientes[0], servicios[0], fecha_futura)
        reservas.append(reserva_sala)
        logger.info(f"ÉXITO: Reserva en memoria. Detalles:\n{reserva_sala.obtener_detalles()}")
    except ReservaInvalidaError as e:
        logger.error(f"FALLO: No se pudo crear reserva: {e}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 6: Confirmar reserva válida calculando costo con descuento e impuesto
    #              (Demostración de sobrecarga y de bloques try/except/else/finally)
    # -------------------------------------------------------------------------
    logger.info("\n--- OPERACIÓN 6: Confirmar Reserva Válida con Descuento e Impuesto (try/except/else/finally) ---")
    if reserva_sala:
        try:
            logger.info("Intentando confirmar reserva...")
            # Sobrecarga de ReservaSala: descuento=$25.0, impuesto=0.19 (19% IVA)
            reserva_sala.confirmar(descuento=25.0, impuesto=0.19)
        except ReservaInvalidaError as e:
            logger.error(f"FALLO: No se pudo confirmar la reserva: {e}")
        else:
            logger.info(f"ÉXITO: Reserva confirmada correctamente.")
            logger.info(f"Costo bruto: $250.00 | Descuento: $25.00 | IVA: 19% | Costo total facturado: ${reserva_sala.costo_final:.2f}")
        finally:
            logger.info("Bloque FINALLY ejecutado: Operación de confirmación finalizada.")

    # -------------------------------------------------------------------------
    # OPERACIÓN 7: Crear servicio de Asesoría Especializada y confirmar reserva con recargo
    # -------------------------------------------------------------------------
    logger.info("\n--- OPERACIÓN 7: Crear y Confirmar Asesoría Especializada (Con Recargo por Urgencia) ---")
    try:
        # Asesoría en Redes, con el consultor Carlos, por 3 horas, tarifa por hora de $120.0
        asesoria = AsesoriaEspecializada("Diseño de Redes", "Carlos Gómez", 3, 120.0)
        servicios.append(asesoria)
        
        # Nueva reserva para el mismo cliente
        reserva_asesoria = Reserva(clientes[0], asesoria, datetime.now() + timedelta(days=5))
        reservas.append(reserva_asesoria)
        
        # Confirmar con opción de urgencia (recargo del 20%)
        reserva_asesoria.confirmar(es_urgente=True)
        logger.info(f"ÉXITO: Reserva de asesoría confirmada:\n{reserva_asesoria.obtener_detalles()}")
    except (ServicioInvalidoError, ReservaInvalidaError) as e:
        logger.error(f"FALLO: Error en el flujo de asesoría: {e}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 8: Crear servicio de Alquiler de Equipos e intentar aplicar descuento excesivo
    #              (Demostración de encadenamiento de excepciones)
    # -------------------------------------------------------------------------
    logger.info("\n--- OPERACIÓN 8: Confirmar Alquiler con Descuento Inválido (Excepción Encadenada) ---")
    try:
        # Alquiler de 2 Laptops, por 4 días, a $30.0 por día
        alquiler = AlquilerEquipos("Laptop Gamer", 2, 4, 30.0)
        servicios.append(alquiler)
        
        reserva_alquiler = Reserva(clientes[0], alquiler, datetime.now() + timedelta(days=3))
        reservas.append(reserva_alquiler)
        
        # Descuento en porcentaje de 1.5 (150%), lo cual es inválido
        logger.info("Intentando confirmar alquiler con descuento del 150%...")
        reserva_alquiler.confirmar(descuento_porcentaje=1.5)
    except ReservaInvalidaError as e:
        logger.warning(f"CONTROLADO: Excepción de reserva capturada con éxito: {e}")
        if e.__cause__:
            logger.warning(f"  --> Causa raíz (excepción original): {e.__cause__}")
        else:
            logger.error("  --> No se encontró la causa raíz de la excepción.")

    # -------------------------------------------------------------------------
    # OPERACIÓN 9: Intento de crear reserva con fecha pasada (Fallo controlado)
    # -------------------------------------------------------------------------
    logger.info("\n--- OPERACIÓN 9: Crear Reserva con Fecha Pasada ---")
    try:
        fecha_pasada = datetime.now() - timedelta(days=1)
        reserva_invalida = Reserva(clientes[0], servicios[0], fecha_pasada)
        reservas.append(reserva_invalida)
    except ReservaInvalidaError as e:
        logger.warning(f"CONTROLADO: Error esperado al crear reserva con fecha pasada: {e}")

    # -------------------------------------------------------------------------
    # OPERACIÓN 10: Intento de cancelar una reserva que ya está cancelada o confirmar una ya confirmada
    # -------------------------------------------------------------------------
    logger.info("\n--- OPERACIÓN 10: Doble Cancelación de una Reserva ---")
    if reserva_sala:
        try:
            logger.info("Cancelando la reserva de sala por primera vez...")
            reserva_sala.cancelar()
            
            logger.info("Intentando cancelar la misma reserva por segunda vez...")
            reserva_sala.cancelar()
        except ReservaInvalidaError as e:
            logger.warning(f"CONTROLADO: Error esperado al cancelar reserva por segunda vez: {e}")

    logger.info("\n======================================================================")
    logger.info("   SIMULACIÓN FINALIZADA - EL SISTEMA CONTINUÓ ESTABLE")
    logger.info("======================================================================")

if __name__ == "__main__":
    iniciar_app()
