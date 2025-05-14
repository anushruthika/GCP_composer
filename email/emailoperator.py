from airflow import DAG
from airflow.operators.email import EmailOperator
from datetime import datetime

# Define the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 5, 14),
}

dag = DAG('send_email_example', default_args=default_args, schedule_interval=None)

# Define the email task
email_task = EmailOperator(
    task_id='send_email',
    to='recipient@example.com',
    subject='Airflow Email Notification',
    html_content='<p>Hello, this is a test email sent by Airflow!</p>', 
# text_content: (Optional) Plain text content of the email.
    dag=dag
)

# Trigger the email task
email_task
