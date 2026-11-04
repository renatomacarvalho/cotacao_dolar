FROM astrocrpublic.azurecr.io/runtime:3.3-11

ENV PYTHONPATH="/usr/local/airflow/include:${PYTHONPATH}"
