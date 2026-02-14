from datetime import date, datetime
from general_helpers import get_vzla_datetime
import math


def calcular_edad(fecha_nacimiento: str) -> int:
    """
    Calcula edad basada en string formato 'aaaa-mm-dd'
    Ejemplo input: '1995-12-23'
    """
    try:
        fecha_dt = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
    except:
        raise Exception("Formato de fecha incorrecto")

    hoy = get_vzla_datetime().date()
    edad = hoy.year - fecha_dt.year

    # Si devuelve True (1), se resta 1 a la edad.
    ajuste = (hoy.month, hoy.day) < (fecha_dt.month, fecha_dt.day)

    return edad - ajuste


def calcular_bsa_mosteller(peso_kg: float, altura_cm: float) -> float:
    """
    Calcula el BSA usando la fórmula de Mosteller.
    Retorna el valor en metros cuadrados (m²) redondeado a 2 decimales.
    """
    if peso_kg <= 0 or altura_cm <= 0:
        return 0.0

    bsa = math.sqrt((peso_kg * altura_cm) / 3600)
    return round(bsa, 2)
