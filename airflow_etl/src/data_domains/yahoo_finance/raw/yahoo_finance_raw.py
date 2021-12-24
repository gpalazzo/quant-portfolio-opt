import pandas as pd
from utils import dump_data_pgsql, read_data_pgsql, load_and_merge_ymls
import yfinance as yf
import os
import time


CONFIG_PATH = [f"{os.getenv('PROJECT_ROOT_PATH')}/conf/yahoo_finance/io.yml"]
config = load_and_merge_ymls(paths=CONFIG_PATH)


def run_yf_stock_prices_raw():

    stock_name = []
    start_date = []
    end_date = []
    data_freq = []
    price_type = []
    status = []

    df_stock_names = read_data_pgsql(
        database=config["yf_stock_names_db_name"],
        tbl_name=config["yf_stock_names_tbl_name"],
    )

    stocks = df_stock_names["stocks_name"].unique().tolist()

    for i, stock in enumerate(stocks, 1):

        time.sleep(1)

        interval = "1d"
        _price_type = "Adj Close"

        print(f"Parsing data for stock: {stock}")
        print(f"Stock {i} out of {len(stocks)} stocks")
        df_stock_prices = yf.download(stock, period="max", interval=interval)[
            _price_type
        ].reset_index()

        stock_name.append(stock)
        data_freq.append(interval)
        price_type.append(_price_type)

        if df_stock_prices.empty:
            start_date.append(None)
            end_date.append(None)
            status.append("no_data")
            print(f"Skipping stock: {stock} because it has no price data")
            continue

        else:
            start_date.append(df_stock_prices["Date"].min())
            end_date.append(df_stock_prices["Date"].max())

            df_stock_prices.loc[:, "yf_stock_name"] = stock

            try:
                dump_data_pgsql(
                    df=df_stock_prices,
                    database=config["yf_raw_stock_prices_db_name"],
                    yf_stock_name=stock,
                )
                status.append("dumped")

            except Exception:
                status.append("dump_failed")

    metadata_df = pd.DataFrame(
        {
            "stock_names": stock_name,
            "start_date": start_date,
            "end_date": end_date,
            "data_frequency": data_freq,
            "price_type": price_type,
            "dump_status": status,
        }
    )

    dump_data_pgsql(
        df=metadata_df,
        database=config["yf_raw_stock_metadata_db_name"],
        tbl_name=config["yf_raw_stock_metadata_tbl_name"],
    )


def run_yf_mktcap_raw():

    df_stock_names = read_data_pgsql(
        database=config["yf_stock_names_db_name"],
        tbl_name=config["yf_stock_names_tbl_name"],
    )

    stocks = (
        df_stock_names[df_stock_names["priority"] == "yes"]["stocks_name"]
        .unique()
        .tolist()
    )

    mktcap_dict = {}

    for i, stock in enumerate(stocks, 1):

        print(f"Parsing data for stock: {stock}")
        print(f"Stock {i} out of {len(stocks)} stocks")

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
