import sys
# Add the path to the api_request folder
sys.path.append('/opt/airflow/api_request')
from load import main
import os
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount


default_args = {
    'description': 'A DAG to orchestrate data',
    'start_date': datetime(2025, 8, 4),
    'catchup':False,
}

dag = DAG(
    dag_id='spotify-api-dbt-orchestrator',
    default_args=default_args,
    schedule = timedelta(days=1)
)

with dag:
    task1 = PythonOperator(
        task_id='ingest_data_task',
        python_callable=main
    )

    task2 = DockerOperator(
        task_id='transform_data_task',
        image='ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
        command= 'run',
        working_dir= '/usr/app',
        mounts= [
            Mount(source = '/Users/youkangshon/Documents/GitHub/Spotify_etl/dbt/my_project',
                  target = '/usr/app',
                  type = 'bind'),
            Mount(source = '/Users/youkangshon/Documents/GitHub/Spotify_etl/dbt/profiles.yml',
                  target = '/root/.dbt/profiles.yml',
                  type = 'bind'),
        ],
        network_mode = 'spotify_etl_default',
        docker_url = 'unix:///var/run/docker.sock',
        auto_remove= 'success'
    )

    task1 >> task2