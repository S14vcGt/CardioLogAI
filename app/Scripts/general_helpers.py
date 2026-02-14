from datetime import datetime
from zoneinfo import ZoneInfo

def get_vzla_datetime():
    # Retorna un objeto datetime con la zona horaria de Vzla
    try:
     return datetime.now(ZoneInfo("America/Caracas"))
    except:
        raise Exception("Error al obtener la zona horaria de Caracas")
