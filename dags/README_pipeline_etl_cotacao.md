# Pipeline ETL de Cotação do Dólar com Apache Airflow

## Sobre o projeto

Este projeto implementa um pipeline de ETL (*Extract, Transform, Load*) em Python, orquestrado pelo Apache Airflow, para consultar a cotação do dólar em relação ao real (USD/BRL), processar o resultado e armazená-lo em um banco PostgreSQL hospedado no Supabase.

O projeto foi desenvolvido como portfólio, com foco em automação de processos de dados, integração com APIs e armazenamento em banco de dados.

## Objetivos

- Automatizar a coleta da cotação do dólar.
- Consumir dados de uma API pública.
- Transformar os dados coletados.
- Armazenar os resultados em um banco PostgreSQL na nuvem.
- Orquestrar e acompanhar as etapas usando o Apache Airflow.

## Arquitetura

```text
API de cotação (AwesomeAPI)
          |
          v
Extração com Python
          |
          v
Transformação dos dados
          |
          v
Carga no Supabase (PostgreSQL)

Apache Airflow: orquestra as tarefas
Docker/Astro CLI: ambiente local de execução
```

## Tecnologias utilizadas

- **Python:** extração, transformação e carga dos dados.
- **Apache Airflow:** orquestração e agendamento do pipeline.
- **Docker:** execução dos serviços em containers.
- **Astro CLI:** gerenciamento do ambiente local do Airflow.
- **REST API:** obtenção da cotação.
- **PostgreSQL / Supabase:** armazenamento dos dados.
- **Psycopg 3:** conexão Python com PostgreSQL.
- **Git e GitHub:** versionamento do projeto.

## Fonte dos dados

A cotação é consultada pela API da AwesomeAPI:

- Endpoint: <https://economia.awesomeapi.com.br/json/last/USD-BRL>
- Documentação: <https://docs.awesomeapi.com.br/api-de-moedas>

A consulta utiliza o par USD-BRL e lê o campo `bid` da resposta.

## Etapas do pipeline

A DAG `pipeline_etl_cotacao` organiza o fluxo em três tarefas.

### 1. Extração — `extrair_cotacao`

- Realiza uma requisição HTTP à API.
- Verifica se a resposta foi bem-sucedida.
- Extrai a cotação do dólar do campo `bid`.
- Converte o valor para um número decimal (`float`).

### 2. Transformação — `processar_dados`

Prepara os campos que serão gravados:

| Campo | Descrição |
|---|---|
| `data_consulta` | Data e hora registradas durante o processamento |
| `valor` | Cotação extraída da API |
| `status` | Classificação baseada no valor da cotação |

Regra de classificação implementada:

- `ALTO`: cotação superior a R$ 5,00.
- `BAIXO`: cotação menor ou igual a R$ 5,00.

O limite de R$ 5,00 é uma regra demonstrativa do projeto, não uma recomendação financeira.

### 3. Carga — `carregar_dados_supabase`

- Abre uma conexão PostgreSQL usando Psycopg 3.
- Insere os campos `data_consulta`, `valor` e `status` na tabela `cotacoes_dolar`.
- Confirma a transação após a inserção.

A tabela `cotacoes_dolar` precisa existir previamente no banco, com colunas compatíveis com os dados inseridos.

## Agendamento

O agendamento é definido na configuração da DAG, no arquivo `dags/etl_supabase.py`.

Se o Airflow estiver configurado em UTC e a expressão for:

```python
schedule='30 11 * * *'
```

a execução está programada diariamente para 11h30 UTC, equivalente a 08h30 no horário de Brasília (UTC−3).

Confirme a configuração atual no código e o próximo horário de execução na interface do Airflow, pois alterações de fuso horário ou de cron mudam esse comportamento.

## Como executar localmente

### Pré-requisitos

- Linux
- Docker
- Astro CLI
- Acesso a um projeto Supabase com PostgreSQL
- Credenciais válidas para conexão com o banco

### 1. Clonar o repositório

Substitua `<URL_DO_REPOSITORIO>` pela URL do seu repositório:

```bash
git clone <URL_DO_REPOSITORIO>
cd airflow-portfolio
```

### 2. Configurar a variável de ambiente

Crie um arquivo `.env` na raiz do projeto:

```dotenv
DB_PASS=sua_senha_do_banco
```

Substitua o valor de exemplo pela senha real. Não publique o arquivo `.env`.

O projeto também utiliza host, nome do banco, usuário e porta definidos no código Python. Para uma configuração mais flexível, considere migrar esses parâmetros para variáveis de ambiente.

**Importante:** o `.env` no computador não é automaticamente disponibilizado em qualquer container. Configure o Astro/Airflow para passar `DB_PASS` ao serviço que executa a tarefa. No ambiente deste projeto, essa variável foi verificada dentro do container do scheduler.

### 3. Iniciar o ambiente

```bash
astro dev start
```

### 4. Acessar a interface do Airflow

Abra <http://localhost:8080>, localize a DAG `pipeline_etl_cotacao` e confira se ela está ativa. Use a interface para acompanhar as tarefas e consultar os logs.

## Segurança

- Não versionar arquivos `.env`.
- Não publicar senhas, tokens ou outras credenciais.
- Usar variáveis de ambiente ou um gerenciador de segredos para informações sensíveis.
- Verificar `git status` antes de fazer commit.
- Se uma senha tiver sido publicada ou compartilhada acidentalmente, alterá-la no serviço correspondente.

Verifique se o `.gitignore` contém pelo menos:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

## Melhorias futuras

- Implementar logs estruturados e tratamento de falhas.
- Evitar registros duplicados em reexecuções.
- Registrar a data/hora da cotação retornada pela API, se disponível, além da hora de processamento.
- Adicionar testes automatizados para as etapas do pipeline.
- Implementar monitoramento e alertas de falha.
- Validar a qualidade dos dados recebidos.
- Centralizar as configurações de conexão em variáveis de ambiente.

## Autor

Projeto de portfólio desenvolvido para praticar integração com APIs, Python, Apache Airflow e PostgreSQL.

GitHub: <https://github.com/renatomacarvalho>
