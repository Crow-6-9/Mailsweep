# gmail_cleaner/dags/delete_emails_dag.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from gmail_cleaner.gmail_utils import GmailCleaner
from gmail_cleaner.auth import GmailAuth

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def run_email_cleanup(label_name="CATEGORY_PROMOTIONS"):
    """This function is triggered by the DAG to delete specific emails."""
    service = GmailAuth().authenticate()
    cleaner = GmailCleaner(service)
    email_ids = cleaner.list_emails(label_name)
    cleaner.delete_emails(email_ids, label_name)

with DAG(
    'email_cleanup_dag',
    default_args=default_args,
    description='Delete Gmail emails from Promotions or Social periodically',
    schedule_interval='@weekly',  
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['gmail', 'cleanup'],
) as dag:

    delete_promotions = PythonOperator(
        task_id='delete_promotions',
        python_callable=run_email_cleanup,
        op_kwargs={'label_name': 'CATEGORY_PROMOTIONS'}
    )

    delete_social = PythonOperator(
        task_id='delete_social',
        python_callable=run_email_cleanup,
        op_kwargs={'label_name': 'CATEGORY_SOCIAL'}
    )

    delete_promotions >> delete_social 
