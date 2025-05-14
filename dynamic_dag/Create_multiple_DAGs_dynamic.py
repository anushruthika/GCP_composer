from airflow.operators.dummy import DummyOperator
from datetime import datetime
from airflow.utils.dates import days_ago

airport_codes = ["atl", "lax", "jfk"]

def create_dag(code):
    with DAG(
        dag_id=f"{code}_daily_etl",
        start_date=datetime(2024, 1, 1, 9, 0),
        schedule_interval="@daily",
        catchup=False,
        tags=["dynamic", "airport"]
    ) as dag:
        start = DummyOperator(task_id='start')
        end = DummyOperator(task_id='end')

        start >> end

        return dag

# Dynamically generate and register DAGs
for code in airport_codes:
    dag_id = f"{code}_daily_etl"
    globals()[dag_id] = create_dag(code)
