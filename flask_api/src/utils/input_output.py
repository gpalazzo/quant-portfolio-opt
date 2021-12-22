import pandas as pd
from sqlalchemy import create_engine
import os


def read_data_pgsql(
    database: str = None, tbl_name: str = None, query: str = None
) -> pd.DataFrame:

    if not database:
        raise Exception("You must provide a database")

    print(f"Reading data from PGSQL")
    engine = create_engine(
        f"postgresql://{os.getenv('PGSQL_USERNAME')}:{os.getenv('PGSQL_PASSWORD')}@{os.getenv('PGSQL_HOST')}:{os.getenv('PGSQL_PORT')}/{database}"
    )

    if not tbl_name and not query:
        raise Exception("Provide either a table name or a query")

    if not query:
        df = pd.read_sql_query(
            f'select * from {database}.public."{tbl_name}"', con=engine
        )

    else:
        pass  # testar execução de query aqui

    return df


def dump_data_pgsql(
    df: pd.DataFrame,
    database: str = None,
    tbl_name: str = None,
    append_data: bool = True,
) -> None:

    if not database or not tbl_name:
        raise Exception("You must provide a database and a table name to dump data")

    print(f"Dumping data to PGSQL")
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
