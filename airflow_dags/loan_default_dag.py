from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def predict_batch():
    # Code to run batch inference
    print("Running prediction batch...")

with DAG(
    dag_id="loan_default_batch_prediction",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",  # run every day
    catchup=False
) as dag:

    predict_task = PythonOperator(
        task_id="predict",
        python_callable=predict_batch
    )
