import yfinance as yf
import pandas as pd
import requests
from typing import List


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


df = yf.download("AAPL", start="2020-02-01", end="2020-03-20")["Adj Close"].reset_index()
print(df)

