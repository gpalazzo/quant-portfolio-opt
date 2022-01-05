from utils import dump_data_pgsql, read_data_pgsql, load_and_merge_ymls
import os
from functools import reduce
import pandas as pd
from sqlalchemy.exc import ProgrammingError
from time import sleep


# reading configs from yml file
CONFIG_PATH = [f"{os.getenv('PROJECT_ROOT_PATH')}/conf/yahoo_finance/io.yml"]
config = load_and_merge_ymls(paths=CONFIG_PATH)


def run_yf_stock_prices_intermediate() -> None:
    """Load, parse and dump stock price data
    It merges all stocks into one single dataframe

    Returns:
        None, it dumps data to a PostgreSQL table instead
    """

    df_stock_names = read_data_pgsql(
        database=config["yf_raw_stock_metadata_db_name"],
        tbl_name=config["yf_raw_stock_metadata_tbl_name"],
    )

    # get only tickers in which data was dumped successfully
    df_stock_names = df_stock_names[df_stock_names["dump_status"] == "dumped"]

    stocks = df_stock_names["stock_names"].unique().tolist()

    dfs = []

    for stock in stocks:

        # give PGSQL some time to close connection, otherwise it will fail due to too many connections
        sleep(0.5)

        try:
            df = read_data_pgsql(
                database=config["yf_raw_stock_prices_db_name"], yf_stock_name=stock
            )
        # in the project's context, it means the table doesn't exist
        except ProgrammingError:
            continue

        df = df.rename(columns={"Adj Close": df["yf_stock_name"].unique()[0]}).drop(
            columns=["yf_stock_name"]
        )
        dfs.append(df)

    # build single dataframe
    all_stocks = reduce(
        lambda left, right: pd.merge(left, right, on="Date", how="outer"), dfs
    )

    dump_data_pgsql(
        df=all_stocks,
        database=config["yf_int_stock_prices_db_name"],
        tbl_name=config["yf_int_stock_prices_tbl_name"],
    )


def run_yf_mktcap_intermediate() -> None:
    """Load, parse and dump market capitalization data

    Returns:
        None, it dumps data to a PostgreSQL table instead
    """

    df = read_data_pgsql(
        database=config["yf_raw_stock_mktcap_db_name"],
        tbl_name=config["yf_raw_stock_mktcap_tbl_name"],
    )

    # get only tickers in which data was dumped successfully
    df = df[df["status"] == "dumped"]

    dump_data_pgsql(
        df=df,
        database=config["yf_int_stock_mktcap_db_name"],
        tbl_name=config["yf_int_stock_mktcap_tbl_name"],
    )
