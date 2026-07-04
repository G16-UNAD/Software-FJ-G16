# Software-FJ-G16
Repositorio del Grupo 16 para el desarrollo de la Fase 4 del proyecto de Programación Orientada a Objetos.

## Integrantes (Grupo 16)
- **CRISTHIAN ADOLFO HERNANDEZ PRIETO**
- **DANIEL ESTEBAN CASTAÑEDA ARANGO**

---

## Descripción del Proyecto
Este sistema es una solución orientada a objetos para la **Gestión de Clientes, Servicios y Reservas** de la empresa **Software FJ**. Implementa conceptos avanzados de POO (abstracción, herencia, polimorfismo y encapsulación), control y encadenamiento de excepciones, logging de auditoría y una interfaz gráfica (GUI) intuitiva en **Tkinter**.

---

## Requisitos Previos
- **Python 3.12+** instalado en el sistema.
- Biblioteca estándar **Tkinter** (se incluye automáticamente en la instalación estándar de Python para Windows).

---

## Instrucciones de Uso y Ejecución

### 1. Iniciar la Aplicación
Para ejecutar el sistema con su interfaz gráfica interactiva, abre una terminal en la carpeta raíz del proyecto y ejecuta:

```bash
py main.py
```
*(o `python main.py` según la configuración de tu sistema).*

### 2. Guía de Módulos en la Interfaz

Al iniciar, se presentará una pantalla de bienvenida y un menú de navegación lateral:

*   **Clientes:** Permite registrar nuevos clientes validando que el correo tenga un formato real, que el teléfono contenga solo números y que los campos obligatorios estén completos. Se muestran listados en una tabla dinámica.
*   **Servicios:** Permite crear dinámicamente tres tipos de servicios especializados mediante formularios específicos:
    1.  *Reserva de Sala* (Capacidad de personas y horas).
    2.  *Alquiler de Equipos* (Cantidad y días).
    3.  *Asesoría Especializada* (Consultor asignado y horas planificadas).
*   **Reservas:** Vincula los clientes y servicios previamente creados.
    *   **Formato de Fecha y Hora:** Se debe ingresar en formato colombiano `DD/MM/YYYY HH:MM` (ej. `28/07/2026 14:30`).
    *   **Soporte de Moneda (COP):** Admite ingresos con formato colombiano (ej. `$50.000` o `1.200.000`) sin generar errores de parsing.
    *   **Acciones:** Haz **doble clic** sobre cualquier reserva registrada en la tabla para abrir la ventana de confirmación (calculando costos finales) o cancelación del registro.
*   **Logs y Simulación:**
    *   Muestra el archivo auditor de registros `app.log` en tiempo real.
    *   Permite ejecutar el simulador automático de las 10 operaciones de consola haciendo clic en **"Ejecutar Simulación"** sin interrumpir la interfaz gráfica.