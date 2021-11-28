from utils import dump_data_pgsql, read_data_pgsql, load_and_merge_ymls
import yfinance as yf
import os
import time


CONFIG_PATH = [f"{os.getenv('PROJECT_ROOT_PATH')}/conf/yahoo_finance/io.yml"]
config = load_and_merge_ymls(paths=CONFIG_PATH)

df = read_data_pgsql(
    database=config["stocks_db_name"], tbl_name=config["stocks_tbl_name"]
)
stocks = df["stocks_name"].unique().tolist()


for i, stock in enumerate(stocks, 1):

    time.sleep(2)

    print(f"Parsing data for stock: {stock}")
    print(f"Stock {i} out of {len(stocks)} stocks")
    df = yf.download(stock, period="max")["Adj Close"].reset_index()

    if df.empty:
        print(f"Skipping stock: {stock} because it has no data")
        continue

    else:
        df.loc[:, "yf_stock_name"] = stock
        dump_data_pgsql(df=df, database=config["yf_raw_db_name"], yf_stock_name=stock)
