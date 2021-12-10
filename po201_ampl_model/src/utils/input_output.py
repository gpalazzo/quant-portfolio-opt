import pandas as pd
from sqlalchemy import create_engine
import os


def dump_data_pgsql(
    df: pd.DataFrame,
    database: str,
    tbl_name: str = None,
    append_data: bool = True,
) -> None:

    print("Dumping data to PGSQL")
    engine = create_engine(
        f"postgresql://{os.getenv('PGSQL_USERNAME')}:{os.getenv('PGSQL_PASSWORD')}@{os.getenv('PGSQL_HOST')}:{os.getenv('PGSQL_PORT')}/{database}"
    )

    try:
        if append_data:
            df.to_sql(tbl_name, engine, if_exists="append", index=False)

        else:
            df.to_sql(tbl_name, engine, if_exists="replace", index=False)

    except Exception as e:
        print("Erro")
        print(e.args)


def read_data_pgsql(
    database: str, tbl_name: str = None, query: str = None
) -> pd.DataFrame:

    print("Reading data from PGSQL")
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
