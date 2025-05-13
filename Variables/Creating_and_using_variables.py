# Define var1 as key with a certain value.
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.models import Variable
from datetime import datetime

def print_var1_python(**kwargs):
    var1_value = Variable.get("var1", default_var="Not Found")
    print(f"PythonOperator: The value of var1 is {var1_value}")

dag = DAG(
    'example_var_usage',
    schedule_interval='@daily',
    start_date=datetime(2023, 5, 12),
    catchup=False
)

python_task = PythonOperator(
    task_id='print_var1_python',
    python_callable=print_var1_python,
    dag=dag
)

bash_task = BashOperator(
    task_id='print_var1_bash',
    bash_command='echo "BashOperator: The value of var1 is {{ var.value.var1 }}"',
    dag=dag
)

python_task >> bash_task
