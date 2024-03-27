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
    , schedule_interval=timedelta(days=180) # update every 6 months
)

# Tasks 
extract_cadastre_task = PythonOperator(
    task_id='extract_cadastre_task'
    , python_callable=extract
    , op_kwargs={
            'url': 'https://cadastre.data.gouv.fr/data/etalab-cadastre/2024-01-01/geojson/departements/13/cadastre-13-parcelles.json.gz'
            , 'save_path': 'data/raw/cadastre_data.geojson'
            }
    , dag=dag
)

trigger_transformation_dag = TriggerDagRunOperator(
    task_id='trigger_transformation_dag',
    trigger_dag_id='offmarket_dag',
    dag=dag,
)

# Deps
extract_cadastre_task >> trigger_transformation_dag