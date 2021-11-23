import pandas as pd
from typing import List
from functools import reduce


def yahoo_finance_primary(*dfs: List[pd.DataFrame]) -> pd.DataFrame:
    # adjust col names for join
    dfs = [
        _df.rename(columns={"Close": _df["Ticker"].unique()[0]}).drop(
            columns=["Ticker"]
        )
        for _df in dfs
    ]

    # build single dataframe
    all_stocks = reduce(lambda left, right: pd.merge(left, right, on="Date"), dfs)

    # parse date format to ISO8601
    all_stocks["Date"] = pd.to_datetime(all_stocks["Date"])

    # lowercase column names
    all_stocks.columns = [col.lower() for col in all_stocks.columns]

    return all_stocks
