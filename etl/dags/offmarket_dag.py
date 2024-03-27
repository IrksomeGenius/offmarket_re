from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from etl.dags.tasks.extract import extract, load, transform

from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow'
    , 'depends_on_past': False
    , 'start_date': datetime(2024,1,1)
    , 'retries': 1
    , 'retry_delay': timedelta(minutes=2)
}

dag = DAG(
    'offmarket_dag'
    , default_args=default_args
    , description='Wait for one of the extract dags to trigger and finish then run the cleaning to get working data + upload it'
    , schedule_interval=None
)


# Tasks 
transform_task = PythonOperator(
    task_id='transform'
    , python_callable=transform
    , dag=dag
)

load_transformed_task = PythonOperator(
    task_id='load_transformed'
    , python_callable=load
    , op_kwargs={'data_type':'transformed'}
    , dag=dag
)

# Deps
transform_task >> load_transformed_task