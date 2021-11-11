import yfinance as yf
import pandas as pd
import requests
from typing import List
from sqlalchemy import create_engine
import os


def parse_stocks_index(target_index: str = "IBXX.SA") -> List[str]:
    """This function uses the `IBXX.SA` index only to find the companies within IBXX

    Args:
        target_index:

    Returns:

    """

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    }
    response = requests.get(
        f"https://finance.yahoo.com/quote/{target_index}/components?p={target_index}",
        headers=headers,
        verify=False,
    )

    df = pd.read_html(response.text)[0]

    return list(set(df["Symbol"]))


try:
    df = yf.download("AAPL", start="2020-02-01", end="2020-03-20")[
        "Adj Close"
    ].reset_index()

    engine = create_engine(
        f"postgresql://{os.getenv('PGSQL_USERNAME')}:{os.getenv('PGSQL_PASSWORD')}@{os.getenv('PGSQL_HOST')}:{os.getenv('PGSQL_PORT')}/raw"
    )
    df.to_sql("ticker_prices", engine, if_exists="replace", index=False)
    print("done!")

except:
    print("fail!")


try:
    print("reading")
    df = pd.read_sql_query('select * from "ticker_prices"', con=engine)
    print(df.head())

except Exception as e:
    print("fail reading")
    print(e.args)
