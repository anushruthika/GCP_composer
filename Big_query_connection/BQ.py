import airflow
import datetime
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.google.cloud.transfers.bigquery_to_gcs import BigQueryToGCSOperator

# Define your dataset, table, bucket, and file names as variables
DATASET_NAME = 'testing'
TABLE = 'A'
BUCKET_NAME = 'us-central1-composername-bucket'
BUCKET_FILE = 'data/address.csv'

# Define default arguments for the DAG
default_dag_args = {
    'start_date': datetime.datetime(2023, 5, 10),  # Use a fixed start date
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id='demo_bq_dag',
    schedule_interval=datetime.timedelta(days=1),
    default_args=default_dag_args,
    catchup=False
) as dag:

    # Task 1: Query from BigQuery using BigQueryInsertJobOperator
    bq_airflow_commits_query = BigQueryInsertJobOperator(
        task_id='bq_airflow_commits_query',
        configuration={
            "query": {
                "query": f"""
                    SELECT *
                    FROM `{DATASET_NAME}.{TABLE}`
                """,
                "useLegacySql": False,  # Use standard SQL
            }
        },
        location='US'  # BigQuery location
    )

    # Task 2: Export BigQuery results to GCS using BigQueryToGCSOperator
    bigquery_to_gcs = BigQueryToGCSOperator(
        task_id="bigquery_to_gcs",
        source_project_dataset_table=f"{DATASET_NAME}.{TABLE}",
        destination_cloud_storage_uris=[f"gs://{BUCKET_NAME}/{BUCKET_FILE}"],
        export_format='CSV'  # Export as CSV
    )

    # Define task dependencies: first run the query, then export to GCS
    bq_airflow_commits_query >> bigquery_to_gcs
