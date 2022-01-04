import pandas as pd
from sqlalchemy import create_engine
import os


def read_data_pgsql(
    database: str, yf_stock_name: str = None, tbl_name: str = None, query: str = None
) -> pd.DataFrame:
    """Read data from a PostgreSQL database. Data source can be any of the following:
        yahoo finance stock name, table name or query

    Args:
        database: str of database name
        yf_stock_name: str of yahoo finance stock name
        tbl_name: str of table name
        query: str of SQL query

    Returns:
        pandas dataframe with the data loaded
    """

    # build sql engine from environment variables
    print(f"Reading data from PGSQL")
    engine = create_engine(
        f"postgresql://{os.getenv('PGSQL_USERNAME')}:{os.getenv('PGSQL_PASSWORD')}@{os.getenv('PGSQL_HOST')}:{os.getenv('PGSQL_PORT')}/{database}"
    )

    # it means the yf stock name should be used as table name
    if yf_stock_name and not tbl_name:
        tbl_name = yf_stock_name.replace(".SA", "").replace("^", "").lower()

    # if no table name was found by any means, then raise error
    if not tbl_name:
        raise Exception("Provide either a table name or a yahoo finance stock name")

    if not query:
        df = pd.read_sql_query(
            f'select * from {database}.public."{tbl_name}"', con=engine
        )

    else:
        # query execution to be implemented
        pass

    return df


def dump_data_pgsql(
    df: pd.DataFrame,
    database: str,
    yf_stock_name: str = None,
    tbl_name: str = None,
    append_data: bool = False,
) -> None:
    """Dumps data to a PostgreSQL table

    Args:
        df: pandas dataframe holding data to be dumped
        database: str of database name
        yf_stock_name: str of yahoo finance stock name
        tbl_name: str of table name
        append_data: boolean to replace or append data to table

    Returns:
        None, it dumps data to a PostgreSQL table instead
    """

    # build sql engine from environment variables
    print(f"Dumping data to PGSQL")
    engine = create_engine(
        f"postgresql://{os.getenv('PGSQL_USERNAME')}:{os.getenv('PGSQL_PASSWORD')}@{os.getenv('PGSQL_HOST')}:{os.getenv('PGSQL_PORT')}/{database}"
    )

    # it means the yf stock name should be used as table name
    if yf_stock_name and not tbl_name:
        tbl_name = yf_stock_name.replace(".SA", "").replace("^", "").lower()

    # if no table name was found by any means, then raise error
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
