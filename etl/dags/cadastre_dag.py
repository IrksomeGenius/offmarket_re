from airflow import DAG
from airflow.operators.python_operator import PythonOperator, TriggerDagRunOperator

from etl.dags.tasks import extract, load

from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow'
    , 'depends_on_past': False
    , 'start_date': datetime(2024,1,1)
    , 'retries': 1
    , 'retry_delay': timedelta(minutes=2)
}

dag = DAG(
    'cadastre_dag'
    , default_args=default_args
    , description='TODO'
    , schedule_interval=timedelta(days=1)
)

# Tasks 
extract_task = PythonOperator(
    task_id='extract_task'
    , python_callable=extract
    , op_kwargs={'extract_type': 'url'
                 , 'call': 'http://example.com/data.csv'
                 , 'save_path': './data/raw/cadastre.csv'}
    , dag=dag
)

trigger_transformation_dag = TriggerDagRunOperator(
    task_id='trigger_transformation_dag',
    trigger_dag_id='offmarket_dag',
    dag=dag,
)

# Deps
extract_task >> trigger_transformation_dag