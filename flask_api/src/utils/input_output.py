import pandas as pd
from sqlalchemy import create_engine
import os


def read_data_pgsql(
    database: str, yf_stock_name: str = None, tbl_name: str = None, query: str = None
) -> pd.DataFrame:

    print(f"Reading data from PGSQL")
    engine = create_engine(
        f"postgresql://{os.getenv('PGSQL_USERNAME')}:{os.getenv('PGSQL_PASSWORD')}@{os.getenv('PGSQL_HOST')}:{os.getenv('PGSQL_PORT')}/{database}"
    )

    if yf_stock_name and not tbl_name:
        tbl_name = yf_stock_name.replace(".SA", "").lower()

    if not tbl_name:
        raise Exception("Provide either a table name or a yahoo finance stock name")

    if not query:
        df = pd.read_sql_query(
            f'select * from {database}.public."{tbl_name}"', con=engine
        )

    else:
        pass  # testar execução de query aqui

    return df


def dump_data_pgsql(
    df: pd.DataFrame,
    database: str,
    yf_stock_name: str = None,
    tbl_name: str = None,
    append_data: bool = False,
) -> None:

    print(f"Dumping data to PGSQL")
    engine = create_engine(
        f"postgresql://{os.getenv('PGSQL_USERNAME')}:{os.getenv('PGSQL_PASSWORD')}@{os.getenv('PGSQL_HOST')}:{os.getenv('PGSQL_PORT')}/{database}"
    )

    if yf_stock_name and not tbl_name:
        tbl_name = yf_stock_name.replace(".SA", "").lower()

    if not tbl_name:
        raise Exception("Provide either a table name or a yahoo finance stock name")

    try:
        if append_data:
            df.to_sql(tbl_name, engine, if_exists="append", index=False)

        else:
            df.to_sql(tbl_name, engine, if_exists="replace", index=False)

    except Exception as e:
        print("Erro")
        print(e.args)
