from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from data_domains.yahoo_finance import (
    run_yf_stock_prices_raw,
    run_yf_mktcap_raw,
    run_stock_names_raw,
    run_yf_stock_prices_intermediate,
    run_yf_mktcap_intermediate,
    run_yf_stock_prices_primary,
    run_yf_mktcap_primary,
)


# stock prices
with DAG(
    dag_id="yf_stock_prices",
    description="All stock prices for yahoo_finance",
    start_date=datetime.now() - timedelta(days=2),
    schedule_interval="*/15 * * * *",
    catchup=False,
) as yf_stock_prices_dag:

    # get stock names
    _yf_stock_names_job = PythonOperator(
        task_id="get_stocks_name",
        python_callable=run_stock_names_raw,
        dag=yf_stock_prices_dag,
    )

    # yahoo finance stock prices raw layer
    _yf_stock_prices_raw_job = PythonOperator(
        task_id="yf_stock_prices_raw",
        python_callable=run_yf_stock_prices_raw,
        dag=yf_stock_prices_dag,
    )

    # yahoo finance stock prices intermediate layer
    _yf_stock_prices_int_job = PythonOperator(
        task_id="yf_stock_prices_int",
        python_callable=run_yf_stock_prices_intermediate,
        dag=yf_stock_prices_dag,
    )

    # yahoo finance stock prices primary layer
    _yf_stock_prices_prm_job = PythonOperator(
        task_id="yf_stock_prices_prm",
        python_callable=run_yf_stock_prices_primary,
        dag=yf_stock_prices_dag,
    )

    # execution precedence
    (
        _yf_stock_names_job
        >> _yf_stock_prices_raw_job
        >> _yf_stock_prices_int_job
        >> _yf_stock_prices_prm_job
    )


# market capitalization
with DAG(
    dag_id="yf_mktcap",
    description="All stock market cap for yahoo_finance",
    start_date=datetime.now() - timedelta(days=2),
    schedule_interval="*/15 * * * *",
    catchup=False,
) as yf_stock_mktcap_dag:

    # get stock names
    _yf_stock_names_job = PythonOperator(
        task_id="get_stocks_name",
        python_callable=run_stock_names_raw,
        dag=yf_stock_mktcap_dag,
    )

    # yahoo finance market cap raw layer
    _yf_stock_mktcap_raw_job = PythonOperator(
        task_id="yf_stock_mktcap_raw",
        python_callable=run_yf_mktcap_raw,
        dag=yf_stock_mktcap_dag,
    )

    # yahoo finance  market cap intermediate layer
    _yf_stock_mktcap_int_job = PythonOperator(
        task_id="yf_stock_mktcap_int",
        python_callable=run_yf_mktcap_intermediate,
        dag=yf_stock_mktcap_dag,
    )

    # yahoo finance  market cap primary layer
    _yf_stock_mktcap_prm_job = PythonOperator(
        task_id="yf_stock_mktcap_prm",
        python_callable=run_yf_mktcap_primary,
        dag=yf_stock_mktcap_dag,
    )

    # execution precedence
    (
        _yf_stock_names_job
        >> _yf_stock_mktcap_raw_job
        >> _yf_stock_mktcap_int_job
        >> _yf_stock_mktcap_prm_job
    )
