from airflow.decorators import dag, task
from datetime import datetime

@dag(
    'simple_dag',
    default_args={'owner': 'airflow'},
    description='A simple DAG',
    schedule_interval='@daily',
    start_date=datetime(2025, 5, 14),
    catchup=False
)
def simple_dag():

    @task()
    def task_1():
        return "Task 1 completed"

    task_1()

simple_dag_instance = simple_dag()
