from airflow.decorators import task
from airflow.operators.dummy import DummyOperator
from datetime import datetime
from airflow import DAG

# Define a simple task using the @task decorator
@task()
def my_task():
    print("This is a task using @task decorator")

# Define the DAG manually
dag = DAG(
    'dag_with_task_decorator_only',
    default_args={'owner': 'airflow'},
    description='A DAG with a task using the @task decorator',
    schedule_interval='@daily',
    start_date=datetime(2025, 5, 14),
    catchup=False
)

# Create the task and add it to the DAG
task_1 = my_task()

# You can still use traditional task dependencies
start = DummyOperator(task_id='start', dag=dag)
end = DummyOperator(task_id='end', dag=dag)

start >> task_1 >> end
