import pandas as pd
from sqlalchemy import create_engine
import os
from typing import List, Any


def read_data_pgsql(
    database: str = None,
    tbl_name: str = None,
    query: str = None,
    filter_params: List[Any] = None,
) -> pd.DataFrame:
    """Read data from a PostgreSQL database

    Args:
        database: str of database name
        tbl_name: str of table name
        query: str of SQL query
        filter_params: list of parameters to be filtered. Specially useful
            by combining `where` and `in` clauses

    Returns:
        pandas dataframe with data from either entire table or query
    """

    if not database:
        raise Exception("You must provide a database")

    # build sql engine from environment variables
    print(f"Reading data from PGSQL")
    engine = create_engine(
        f"postgresql://{os.getenv('PGSQL_USERNAME')}:{os.getenv('PGSQL_PASSWORD')}@{os.getenv('PGSQL_HOST')}:{os.getenv('PGSQL_PORT')}/{database}"
    )

    if not tbl_name and not query:
        raise Exception("Provide either a table name or a query")

    if not query:
        # table name must be within double quotes ""
        df = pd.read_sql_query(
            f'select * from {database}.public."{tbl_name}"', con=engine
        )

    else:
        if not filter_params:
            df = pd.read_sql_query(query, con=engine)

        else:
            cursor = engine.raw_connection().cursor()
            # execute query by dynamically adding parameters
            cursor.execute(query, filter_params)
            df = pd.DataFrame(cursor.fetchall())
            df.columns = cursor.keys()

    return df


def dump_data_pgsql(
    df: pd.DataFrame,
    database: str = None,
    tbl_name: str = None,
    append_data: bool = True,
) -> None:
    """Dumps data to a PostgreSQL table

    Args:
        df: pandas dataframe holding data to be dumped
        database: str of database name
        tbl_name: str of table name
        append_data: boolean to replace or append data to table

    Returns:
        None, it dumps data to a PostgreSQL table instead
    """

    if not database or not tbl_name:
        raise Exception("You must provide a database and a table name to dump data")

    # build sql engine from environment variables
    print(f"Dumping data to PGSQL")
    engine = create_engine(
        f"postgresql://{os.getenv('PGSQL_USERNAME')}:{os.getenv('PGSQL_PASSWORD')}@{os.getenv('PGSQL_HOST')}:{os.getenv('PGSQL_PORT')}/{database}"
    )

    try:
        if append_data:
            df.to_sql(tbl_name, engine, if_exists="append", index=False)

        else:
            df.to_sql(tbl_name, engine, if_exists="replace", index=False)

    # dummy error args printing for debugging purposes
    except Exception as e:
        print("Erro")
        print(e.args)
