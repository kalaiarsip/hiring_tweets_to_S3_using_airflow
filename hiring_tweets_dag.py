from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
from tweets_hiring import get_hiring_tweets_to_s3

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 11, 8),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'hiring_tweets_s3_dag',
    default_args=default_args,
    description='ETL for tweets related to hiring tweets in data domain',
    schedule_interval=timedelta(days=1),
)

dag = DAG(
    'twitter_dag',
    default_args=default_args,
    description='ETL for tweets related to hiring tweets in data domain'
)

run_etl = PythonOperator(
    task_id='complete_twitter_etl',
    python_callable=get_hiring_tweets_to_s3,
    dag=dag, 
)

run_etl
