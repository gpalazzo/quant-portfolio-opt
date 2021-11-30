import pandas as pd
from utils import dump_data_pgsql, read_data_pgsql, load_and_merge_ymls
import yfinance as yf
import os
import time


CONFIG_PATH = [f"{os.getenv('PROJECT_ROOT_PATH')}/conf/yahoo_finance/io.yml"]
config = load_and_merge_ymls(paths=CONFIG_PATH)

df_stock_names = read_data_pgsql(
    database=config["yf_stock_names_db_name"],
    tbl_name=config["yf_stock_names_tbl_name"],
)


def run_yf_stock_prices_raw():

    stocks = df_stock_names["stocks_name"].unique().tolist()

    for i, stock in enumerate(stocks, 1):

        time.sleep(1)

        print(f"Parsing data for stock: {stock}")
        print(f"Stock {i} out of {len(stocks)} stocks")
        df_stock_prices = yf.download(stock, period="max", interval="1mo")[
            "Adj Close"
        ].reset_index()

        if df_stock_prices.empty:
            print(f"Skipping stock: {stock} because it has no price data")
            continue

        else:
            df_stock_prices.loc[:, "yf_stock_name"] = stock
            dump_data_pgsql(
                df=df_stock_prices,
                database=config["yf_raw_stock_prices_db_name"],
                yf_stock_name=stock,
            )


def run_yf_mktcap_raw():

    stocks = (
        df_stock_names[df_stock_names["priority"] == "yes"]["stocks_name"]
        .unique()
        .tolist()
    )

    mktcap_dict = {}

    for i, stock in enumerate(stocks, 1):

        try:
            stock_mktcap = yf.Ticker(stock).info["marketCap"]
        except KeyError:
            stock_mktcap = None

        if stock_mktcap is None or stock_mktcap == 0:
            print(f"Skipping stock: {stock} because it has no market cap data")
            continue

        else:
            mktcap_dict[stock] = stock_mktcap

    df_stock_mktcap = pd.DataFrame(
        {"stocks": mktcap_dict.keys(), "mktcap": mktcap_dict.values()}
    )

    dump_data_pgsql(
        df=df_stock_mktcap,
        database=config["yf_raw_stock_mktcap_db_name"],
        tbl_name=config["yf_raw_stock_mktcap_tbl_name"],
    )
