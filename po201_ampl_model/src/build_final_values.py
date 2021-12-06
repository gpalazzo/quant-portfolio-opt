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


df = read_data_pgsql(database="aux", tbl_name="ampl_report")
_df = df.sort_values(by="run_timestamp", ascending=False).head(1)
_uuid = _df["uuid"].unique().tolist()[0]
df_filter = df[df["uuid"] == _uuid]
start_time = df_filter["run_timestamp"].min()
end_time = df_filter["run_timestamp"].max()
runtime = end_time - start_time
max_return = df_filter["return"].max()
df_final = df_filter[df_filter["return"] == max_return]

breakpoint()

df = read_data_pgsql(database="aux", tbl_name="ga_report")
_df = df.sort_values(by="run_timestamp", ascending=False).head(1)
_uuid = _df["uuid"].unique().tolist()[0]
df_filter = df[df["uuid"] == _uuid]
max_return = df_filter["return"].max()
df_final = df_filter[df_filter["return"] == max_return]

df2 = read_data_pgsql(database="aux", tbl_name="ga_run_time")
df2_filter = df2[df2["uuid"] == _uuid]
breakpoint()
