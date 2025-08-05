import sys
import os
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

# Add the path to the api_request folder
sys.path.append('/opt/airflow/api_request')
print("sys.path:", sys.path)

def safe_main_callable():
    from load import main
    return main()

def example_task():
    print("this is an example task")

default_args = {
    'description': 'A DAG to orchestrate data',
    'start_date': datetime(2025, 8, 4),
    'catchup':False,
}

dag = DAG(
    dag_id='spotify-etl-orchestrator',
    default_args=default_args,
    schedule = timedelta(days=1)
)

with dag:
    task1 = PythonOperator(
        task_id='ingest_data_task',
        python_callable=safe_main_callable
    )