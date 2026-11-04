import requests

def extrair_cotacao():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    dados = response.json()
    valor_dolar = float(dados["USDBRL"]["bid"])
    print(f"[EXTRACT] Cotação do dólar: R$ {valor_dolar:.4f}")
    return valor_dolar    

