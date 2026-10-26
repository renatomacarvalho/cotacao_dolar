from datetime import datetime, timedelta
import requests
import psycopg  # Conector moderno (v3) que instalamos
from airflow.decorators import dag, task
# ==============================================================================
# PASSO 2: COLE AQUI AS SUAS CREDENCIAIS DO SUPABASE (Vem do painel Settings > Database)
# ==============================================================================
DB_HOST = "aws-0-us-east-1.pooler.supabase.com"  # Ex: ://supabase.com
DB_NAME = "postgres"
DB_USER = "postgres.lupssdmiwasyheolmkbr"
DB_PORT = "5432"

import os
from dotenv import load_dotenv

load_dotenv()


DB_PASS = os.getenv("DB_PASS")

# ==============================================================================

default_args = {
    'owner': 'renato',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    dag_id='pipeline_etl_cotacao',
    default_args=default_args,
    description='Pipeline ETL gravando dados no Supabase com Psycopg3',
    schedule='05 08 * * *',
    catchup=False,
    tags=['portfolio', 'postgres', 'supabase', 'etl']
)
def pipeline_cambio_cloud():

    @task()
    def extrair_cotacao():
        url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        dados = response.json()
        valor_dolar = float(dados["USDBRL"]["bid"])
        print(f"[EXTRACT] Cotação do dólar: R$ {valor_dolar:.4f}")
        return valor_dolar    

    @task()
    def processar_dados(valor_dolar: float):
        status = "ALTO" if valor_dolar > 5.0 else "BAIXO"
        return {
            'data_consulta': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'valor': valor_dolar,
            'status': status
        }

    @task()
    def carregar_dados_supabase(dados_processados: dict):
        # Conecta no banco em nuvem usando a biblioteca nova
        conn = psycopg.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        cursor = conn.cursor()
        
        insert_query = """
        INSERT INTO cotacoes_dolar (data_consulta, valor, status)
        VALUES (%s, %s, %s);
        """
        
        cursor.execute(insert_query, (
            dados_processados['data_consulta'],
            dados_processados['valor'],
            dados_processados['status']
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        print("[LOAD] Dados salvos com sucesso no Supabase!")

    # Definindo a ordem de execução (Workflow)
    cotacao = extrair_cotacao()
    dados_finais = processar_dados(cotacao)
    carregar_dados_supabase(dados_finais)

pipeline_cambio_cloud()