import yfinance as yf
import yahoo_fin.stock_info as si
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


#
#
# # BRAX11 é o ETF que replica a performance do IBrX-100: índice com as 100 ações mais líquidas da Bovespa
# mkt_index = "BRAX11.SA"
top30_stocks = parse_stocks_index()
#
# # MARKET INDEX CLOSE PRICE DATA
# mkt_index_close_price = yf.download(tickers=mkt_index, period="max", interval="1d")[
#     "Adj Close"
# ].reset_index()
#
# mkt_index_close_price.to_csv("../data/raw/mkt_index_price_brax11.csv", index=False)
#
# # TOP 30 IBXX (IBRX-100) STOCKS CLOSE PRICE DATA
# index_min_date = mkt_index_close_price["Date"].min()
#
# tickers_close_prices = yf.download(tickers=top30_stocks, period="max", interval="1d")[
#     "Adj Close"
# ].reset_index()
#
# tickers_close_prices = tickers_close_prices[
#     tickers_close_prices["Date"] >= index_min_date
# ]
#
# tickers_close_prices.to_csv(
#     "../data/raw/top30_stocks_price_within_brax11.csv", index=False
# )
#
# # TOP 30 IBXX (IBRX-100) STOCKS MARKET CAPITALIZATION DATA
# mkt_cap_dict = {}
# for ticker in top30_stocks:
#     print(f"Getting market cap data for: {ticker}...")
#     stock = yf.Ticker(ticker)
#     mkt_cap_dict[ticker] = stock.info["marketCap"]
#
#
# mkt_cap_30stocks = (
#     pd.DataFrame.from_dict(mkt_cap_dict, orient="index")
#     .reset_index()
#     .rename(columns={0: "mkt_cap", "index": "ticker"})
# )
#
# mkt_cap_30stocks.to_csv(
#     "../data/raw/top30_stocks_mktcap_within_brax11.csv", index=False
# )

# DADOS PARA A REGRESSÃO MÚLTIPLA
# tickers = ["USDBRL=X"]
# df = yf.download(tickers=tickers, period="max", interval="1d")[
#     "Adj Close"
# ].reset_index()
# df.to_csv("../data/raw/usdbrl_fx.csv", index=False)

# income_dict = {}
for ticker in top30_stocks:
    df_income = si.get_income_statement(ticker=ticker)
    df_transposed = df_income.transpose()
    df_parsed = df_transposed[["grossProfit"]]
    breakpoint()
