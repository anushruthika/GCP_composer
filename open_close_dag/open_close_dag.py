from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

# Python function for the first task
def say_open():
    print("Open")

# Define the DAG
with DAG(
    dag_id='simple_open_close_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['example']
) as dag:

    # Task 1: PythonOperator to say "Open"
    open_task = PythonOperator(
        task_id='say_open',
        python_callable=say_open
    )

    # Task 2: BashOperator to say "Close"
    close_task = BashOperator(
        task_id='say_close',
        bash_command='echo "Close"'
    )

    # Set the task order
    open_task >> close_task
