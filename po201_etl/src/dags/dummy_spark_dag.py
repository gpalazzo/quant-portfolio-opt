# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from datetime import datetime, timedelta
# from data_domains.yahoo_finance import dummy_pyspark_raw
#
#
# # yahoo_finance pyspark
# with DAG(
#     dag_id="dummy_pyspark",
#     description="All tasks for yahoo_finance pyspark",
#     start_date=datetime.now() - timedelta(days=2),
#     schedule_interval="*/15 * * * *",
#     catchup=False,
# ) as dag:
#
#     # raw data layer
#     _dummy_pyspark_raw = PythonOperator(
#         task_id="dummy_pyspark_raw", python_callable=dummy_pyspark_raw, dag=dag
#     )
#
#     # execution precedence
#     _dummy_pyspark_raw
