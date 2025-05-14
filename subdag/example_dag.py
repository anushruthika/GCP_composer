# the code most likely to be present in airflow.example_dags.subdags.subdag
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

def subdag(parent_dag_name, child_dag_name, args):
    """
    This is where tasks like task_1, task_2, etc., are defined for the subDAG.
    """
    dag_subdag = DAG(
        dag_id=child_dag_name,
        default_args=args,
        schedule_interval="@once",
    )

    with dag_subdag:
        task_1 = DummyOperator(task_id='task_1')
        task_2 = DummyOperator(task_id='task_2')
        task_3 = DummyOperator(task_id='task_3')
        task_4 = DummyOperator(task_id='task_4')
        task_5 = DummyOperator(task_id='task_5')

        # Task dependencies within the subDAG
        task_1 >> task_2 >> task_3 >> task_4 >> task_5

    return dag_subdag
