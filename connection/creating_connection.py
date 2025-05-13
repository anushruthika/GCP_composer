import datetime
from airflow import models
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

yesterday = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(1),
    datetime.datetime.min.time())

default_dag_args = {
    'start_date': yesterday,
}

with models.DAG(
    'composer_sample_connections',
    schedule_interval=datetime.timedelta(days=1),
    default_args=default_dag_args,
    catchup=False
) as dag:

    task_default = BigQueryInsertJobOperator(
        task_id='task_default_connection',
        configuration={
            "query": {
                "query": "SELECT 1",
                "useLegacySql": False,
            }
        },
        location='US'  # Set your BigQuery location
    )

    task_explicit = BigQueryInsertJobOperator(
        task_id='task_explicit_connection',
        configuration={
            "query": {
                "query": "SELECT 1",
                "useLegacySql": False,
            }
        },
        gcp_conn_id='google_cloud_default',
        location='US'
    )

    task_custom = BigQueryInsertJobOperator(
        task_id='task_custom_connection',
        configuration={
            "query": {
                "query": "SELECT 1",
                "useLegacySql": False,
            }
        },
        gcp_conn_id='my_gcp_connection',
        location='US'
    )
