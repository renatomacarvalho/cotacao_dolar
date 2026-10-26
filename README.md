# Pipeline ETL de Cotação do Dólar com Apache Airflow

## Sobre o projeto

Este projeto implementa um pipeline de ETL (Extract, Transform, Load) em Python, orquestrado pelo Apache Airflow, para consultar a cotação do dólar em relação ao real (USD/BRL), processar o resultado e armazená-lo em um banco PostgreSQL hospedado no Supabase.

O pipeline foi desenvolvido como projeto de portfólio, com foco em automação de processos de dados, integração com APIs e armazenamento em banco de dados.

## Objetivos

- Automatizar a coleta diária da cotação do dólar.
- Consumir dados de uma API pública.
- Aplicar uma transformação simples aos dados coletados.
- Armazenar os resultados em um banco PostgreSQL na nuvem.
- Utilizar o Apache Airflow para orquestrar e agendar as etapas do processo.

## Arquitetura

```text
API de cotação
      |
      v
Extração com Python
      |
      v
Transformação dos dados
      |
      v
Gravação no Supabase
(PostgreSQL)
```

O Apache Airflow coordena as etapas do pipeline, enquanto o Docker é utilizado no ambiente local de execução.

## Tecnologias utilizadas

- **Python:** extração, processamento e integração com o banco.
- **Apache Airflow:** orquestração, agendamento e acompanhamento das tarefas.
- **Docker:** execução do ambiente do Airflow em containers.
- **REST API:** obtenção da cotação do dólar.
- **PostgreSQL:** armazenamento dos dados.
- **Supabase:** hospedagem do banco de dados.
- **Psycopg 3:** conexão entre Python e PostgreSQL.
- **Git e GitHub:** versionamento e publicação do projeto.

## Fonte dos dados

A cotação é consultada por meio da API da AwesomeAPI:

https://economia.awesomeapi.com.br/json/last/USD-BRL

A consulta utiliza o par de moedas USD-BRL e obtém o valor de compra do dólar informado no campo `bid`.

Documentação da API:

https://docs.awesomeapi.com.br/api-de-moedas

## Etapas do pipeline

### 1. Extração

A tarefa `extrair_cotacao` realiza uma requisição HTTP à API, valida a resposta e extrai a cotação do dólar.

### 2. Transformação

A tarefa `processar_dados` organiza os dados e cria três campos:

- `data_consulta`: data e hora do processamento.
- `valor`: cotação obtida na API.
- `status`: classificação baseada no valor da cotação.

Regra de classificação utilizada:

- `ALTO`: cotação superior a R$ 5,00.
- `BAIXO`: cotação menor ou igual a R$ 5,00.

O limite de R$ 5,00 é uma regra demonstrativa do projeto, não uma recomendação financeira.

### 3. Carga

A tarefa `carregar_dados_supabase` conecta-se ao PostgreSQL por meio do Psycopg 3 e insere os registros na tabela `cotacoes_dolar`.

Campos gravados:

| Campo | Finalidade |
|---|---|
| `data_consulta` | Data e hora da consulta |
| `valor` | Cotação do dólar |
| `status` | Classificação da cotação |

A conexão utiliza uma variável de ambiente para a senha do banco, evitando que esse segredo precise ficar diretamente no código Python.

## Agendamento

O pipeline é executado pelo Apache Airflow uma vez por dia.

O horário configurado é 08h30, no horário de Brasília (America/Sao_Paulo), equivalente a 11h30 UTC quando a DAG utiliza o fuso UTC.

O agendamento pode ser configurado por meio de uma expressão cron no arquivo da DAG.

## Como executar localmente

### Pré-requisitos

- Linux
- Docker
- Astro CLI
- Acesso a um projeto Supabase com PostgreSQL
- Credenciais válidas para conexão com o banco

### 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd airflow-portfolio
```

### 2. Configurar a senha

Crie um arquivo `.env` na raiz do projeto com a variável necessária:

```dotenv
DB_PASS=sua_senha_do_banco
```

Substitua o valor de exemplo pela senha real. Não publique esse arquivo no GitHub.

### 3. Iniciar o ambiente

```bash
astro dev start
```

### 4. Acessar o Airflow

Abra no navegador:

http://localhost:8080

Localize a DAG `pipeline_etl_cotacao`, confira se ela está ativa e acompanhe as tarefas pela interface.

## Segurança

- Não versionar arquivos `.env`.
- Não publicar senhas, tokens ou outras credenciais.
- Utilizar variáveis de ambiente para informações sensíveis.
- Manter as credenciais de acesso ao Supabase protegidas.

## Melhorias futuras

- Implementar logs estruturados e tratamento de falhas.
- Evitar registros duplicados em reexecuções.
- Armazenar o histórico de cotações para análises temporais.
- Criar testes automatizados para as etapas do pipeline.
- Adicionar monitoramento das execuções e alertas de falha.
- Implementar validações adicionais dos dados recebidos.

## Autor

Projeto desenvolvido para fins de estudo e portfólio em engenharia de dados.

GitHub: https://github.com/renatomacarvalho
 ran 'astro dev init' using the Astronomer CLI. This readme describes the contents of the project, as well as how to run Apache m the Open Notify API and prints a statement for each astronaut. The Dag uses the TaskFlow API to define tasks in Python, and dynamic task mapping to dynamically print a statement for each astronaut. For more on how this Dag works, see our [Getting started tutorial](https://www.astronomer.io/docs/learn/get-started-with-airflow).
- Dockerfile: This file contains a versioned Astro Runtime Docker image that provides a differentiated Airflow experience. If you want to execute other commands orach for a different Airflow component:- Postgres: Airflow's Metadata Database- Scheduler: The Airflow component responsible for monitoring and triggering task- Dag Processor: The Airflow component responsible for parsing Dags- API Server: The Airflow component responsible for serving the Airflow UI and API- Triggerer: The Airflow component responsible for triggering defeWhen all five containers are ready the command will open the browser to the Airflow UI at http://localhost:8080/. You shoul
