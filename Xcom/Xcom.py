from __future__ import print_function
import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2),
    'provide_context': True,
}

dag = DAG('XCOM_Dag', schedule_interval="@once", default_args=args)

data_1 = [1, 2, 3]
data_2 = {'a': 'b'}

def push_data(**kwargs):
    """Pushes an XCom without a specific target"""
    kwargs['ti'].xcom_push(key='data from pusher 1', value=data_1)

def push_data_by_returning(**kwargs):
    """Pushes an XCom without a specific target, just by returning it"""
    return data_2

def pull_data(**kwargs):
    ti = kwargs['ti']

    # get data_1
    d1 = ti.xcom_pull(key=None, task_ids='push_data')
    assert d1 == data_1

    # get data_2
    d2 = ti.xcom_pull(task_ids='push_data_by_returning')
    assert d2 == data_2

    # get both data_1 and data_2
    d1, d2 = ti.xcom_pull(key=None, task_ids=['push_data', 'push_data_by_returning'])
    print('Data 1:', d1)
    print('Data 2:', d2)
    assert (d1, d2) == (data_1, data_2)

push_task1 = PythonOperator(
    task_id='push_data',
    dag=dag,
    python_callable=push_data,
)

push_task2 = PythonOperator(
    task_id='push_data_by_returning',
    dag=dag,
    python_callable=push_data_by_returning,
)

pull_task = PythonOperator(
    task_id='pull_data',
    dag=dag,
    python_callable=pull_data,
)

pull_task << [push_task1, push_task2]
