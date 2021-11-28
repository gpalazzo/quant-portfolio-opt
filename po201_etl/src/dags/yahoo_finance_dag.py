from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from data_domains.yahoo_finance import (
    run_yahoo_finance_raw,
    run_yahoo_finance_intermediate,
    run_yahoo_finance_primary,
    run_stock_names_raw,
)


# yahoo finance
with DAG(
    dag_id="yahoo_finance",
    description="All tasks for yahoo_finance",
    start_date=datetime.now() - timedelta(days=2),
    schedule_interval="*/15 * * * *",
    catchup=False,
) as dag:

    # get stock names
    _stocks_job = PythonOperator(
        task_id="get_stocks_name", python_callable=run_stock_names_raw, dag=dag
    )

    # yahoo finance raw layer
    _yf_raw_job = PythonOperator(
        task_id="yf_raw", python_callable=run_yahoo_finance_raw, dag=dag
    )

    # yahoo finance intermediate layer
    _yf_int_job = PythonOperator(
        task_id="yf_int", python_callable=run_yahoo_finance_intermediate, dag=dag
    )

    # yahoo finance primary layer
    _yf_prm_job = PythonOperator(
        task_id="yf_prm", python_callable=run_yahoo_finance_primary, dag=dag
    )

    # execution precedence
    _stocks_job >> _yf_raw_job >> _yf_int_job >> _yf_prm_job
