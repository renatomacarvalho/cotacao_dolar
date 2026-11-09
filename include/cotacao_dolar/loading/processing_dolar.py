import requests
from datetime import datetime

def processing_data(valor_dolar: float):
    status = "ALTO" if valor_dolar > 5.0 else "BAIXO"

    return {
        "data_consulta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "valor": valor_dolar,
        "status": status
    }        