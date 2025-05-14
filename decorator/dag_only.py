from airflow.decorators import dag
from airflow.operators.dummy import DummyOperator
from datetime import datetime

@dag(
    'dag_without_task_decorator',
    default_args={'owner': 'airflow'},
    description='A DAG without the @task decorator',
    schedule_interval='@daily',
    start_date=datetime(2025, 5, 14),
    catchup=False
)
def my_dag():
    task_1 = DummyOperator(task_id='task_1')
    task_2 = DummyOperator(task_id='task_2')

    task_1 >> task_2  # Define task dependencies

my_dag_instance = my_dag()
