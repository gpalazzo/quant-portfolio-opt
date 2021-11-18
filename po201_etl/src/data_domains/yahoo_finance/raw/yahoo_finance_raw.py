import pandas as pd
from sqlalchemy import create_engine
import os


try:
    df = pd.read_csv("/opt/airflow/data/yahoo_finance/raw/hdfc.csv")

    engine = create_engine(
        f"postgresql://{os.getenv('PGSQL_USERNAME')}:{os.getenv('PGSQL_PASSWORD')}@{os.getenv('PGSQL_HOST')}:{os.getenv('PGSQL_PORT')}/raw"
    )
    df.to_sql("hdfc", engine, if_exists="replace", index=False)
    print("done!")

except:
    print("fail!")


try:
    print("reading")
    df = pd.read_sql_query('select * from "hdfc"', con=engine)
    print(df.head())

except Exception as e:
    print("fail reading")
    print(e.args)
