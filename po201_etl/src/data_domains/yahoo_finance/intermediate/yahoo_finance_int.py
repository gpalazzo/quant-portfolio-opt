from utils import dump_data_pgsql, read_data_pgsql, load_and_merge_ymls
import os
from functools import reduce
import pandas as pd


CONFIG_PATH = [f"{os.getenv('PROJECT_ROOT_PATH')}/conf/yahoo_finance/io.yml"]
config = load_and_merge_ymls(paths=CONFIG_PATH)

df = read_data_pgsql(
    database=config["yf_stock_names_db_name"],
    tbl_name=config["yf_stock_names_tbl_name"],
)
stocks = df["stocks_name"].unique().tolist()


def run_yf_stock_prices_intermediate():

    dfs = []

    for stock in stocks:
        df = read_data_pgsql(
            database=config["yf_raw_stock_prices_db_name"], yf_stock_name=stock
        )
        if df.empty:
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


def run_yf_mktcap_intermediate():

    df = read_data_pgsql(
        database=config["yf_raw_stock_mktcap_db_name"],
        tbl_name=config["yf_raw_stock_mktcap_tbl_name"],
    )

    dump_data_pgsql(
        df=df,
        database=config["yf_int_stock_mktcap_db_name"],
        tbl_name=config["yf_int_stock_mktcap_tbl_name"],
    )
