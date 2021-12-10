import pandas as pd
from sqlalchemy import create_engine
import os


def read_data_pgsql(
    database: str, tbl_name: str = None, query: str = None
) -> pd.DataFrame:

    print(f"Reading data from PGSQL")
    engine = create_engine(
        f"postgresql://{os.getenv('PGSQL_USERNAME')}:{os.getenv('PGSQL_PASSWORD')}@{os.getenv('PGSQL_HOST')}:{os.getenv('PGSQL_PORT')}/{database}"
    )

    if not query:
        df = pd.read_sql_query(
            f'select * from {database}.public."{tbl_name}"', con=engine
        )

    else:
        pass  # testar execução de query aqui

    return df


df = read_data_pgsql(database="aux", tbl_name="ampl_markowitz")
excl_cols = ["run_timestamp", "total_run_time_min", "solve_time_min", "mean", "risk"]
select_cols = list(set(df.columns.tolist()) - set(excl_cols))
print(f"Soma dos pesos: {df[select_cols].sum().sum()}")
breakpoint()
