from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

with DAG('task_group_example', default_args=default_args, schedule_interval=None) as dag:

    start = DummyOperator(task_id='start')

    # Define a TaskGroup
    with TaskGroup("group_1", tooltip="This is the first group of tasks") as group_1:
        task_1 = DummyOperator(task_id='task_1')
        task_2 = DummyOperator(task_id='task_2')
        task_3 = DummyOperator(task_id='task_3')

    end = DummyOperator(task_id='end')

    start >> group_1 >> end
