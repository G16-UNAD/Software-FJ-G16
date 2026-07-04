# src/gui/utils.py
import re

def limpiar_y_parsear_costo(costo_str):
    """
    Limpia y parsea un string de costo al formato float de Python.
    Soporta formato colombiano:
    - Omitir símbolo de moneda ($) y espacios.
    - Tratar el punto (.) como separador de miles si hay comas o si se usa como tal.
    """
    s = costo_str.strip().replace("$", "").replace(" ", "")
    if not s:
        raise ValueError("El campo está vacío.")
    
    puntos = s.count(".")
    comas = s.count(",")
    
    if puntos > 0 and comas > 0:
        pos_punto = s.rfind(".")
        pos_coma = s.rfind(",")
        if pos_punto > pos_coma:
            s = s.replace(",", "")
        else:
            s = s.replace(".", "").replace(",", ".")
    elif comas > 0:
        if comas > 1:
            s = s.replace(",", "")
        else:
            partes = s.split(",")
            if len(partes[1]) == 3:
                s = s.replace(",", "")
            else:
                s = s.replace(",", ".")
    elif puntos > 0:
        if puntos > 1:
            s = s.replace(".", "")
        else:
            partes = s.split(".")
            if len(partes[1]) == 3:
                s = s.replace(".", "")
    
    return float(s)

def formatear_moneda_cop(valor):
    if valor is None:
        return "$0,00"
    us_format = f"{valor:,.2f}"
    temp = us_format.replace(",", "TEMP")
    temp = temp.replace(".", ",")
    cop_format = temp.replace("TEMP", ".")
    return f"${cop_format}"
