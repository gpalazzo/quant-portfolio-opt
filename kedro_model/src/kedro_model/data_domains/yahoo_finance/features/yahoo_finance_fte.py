import pandas as pd
import numpy as np
from typing import List
from datetime import timedelta, datetime


def yahoo_finance_features(
    df_opt_requests: pd.DataFrame,
    df: pd.DataFrame,
    days_roll_window: List[int],
    days_lookback: int,
    null_pct_cut: float,
) -> pd.DataFrame:

    final_df = pd.DataFrame()

    for uuid in df_opt_requests["uuid"].unique().tolist():

        df_aux = df_opt_requests[df_opt_requests["uuid"] == uuid]

        tickers = str(df_aux["tickers"].unique().tolist())

        # TODO: substituir esses replaces por regex
        tickers = [
            ticker.strip()
            .lower()
            .replace(".sa", "")
            .replace("'", "")
            .replace("[", "")
            .replace("]", "")
            for ticker in tickers.split(",")
        ]

        df = df[["date"] + tickers]

        df_pre_processed = _yf_fte_pre_processing(
            df=df, days_lookback=days_lookback, null_pct_cut=null_pct_cut
        )

        df_ftes = _yf_calculate_rolling_windows(
            df=df_pre_processed, days_roll_window=days_roll_window
        )

        df_ftes.loc[:, "uuid"] = uuid

        final_df = final_df.append(df_ftes)

    return final_df


def yf_select_mktcap_tickers(
    df_stocks_mktcap: pd.DataFrame, df_stocks_prices: pd.DataFrame
) -> pd.DataFrame:

    selected_stocks = df_stocks_prices.T.index.tolist()

    df_stocks_selected_mktcap = df_stocks_mktcap[
        df_stocks_mktcap["stocks"].isin(selected_stocks)
    ]

    return df_stocks_selected_mktcap


def _yf_fte_pre_processing(
    df: pd.DataFrame, days_lookback: int, null_pct_cut: float
) -> pd.DataFrame:

    lower_bound_date = datetime.today() - timedelta(days=days_lookback)

    # filter date
    df_filter_date = df[df["date"] >= lower_bound_date]

    # filter null percentage
    _mask = df_filter_date.isna().mean()
    df_filter_null = df_filter_date.loc[:, _mask <= null_pct_cut]

    # input nulls
    #   get columns with null value
    null_cols = df_filter_null.columns[df_filter_null.isna().any()].tolist()

    #   input with linear interpolation and backfill
    for col in null_cols:
        df_filter_null[col] = (
            df_filter_null[col].interpolate(method="linear").fillna(method="bfill")
        )

    assert (
        df_filter_null.isnull().sum().sum() == 0
    ), "There's still missing values, verify"

    return df_filter_null


def _yf_calculate_rolling_windows(
    df: pd.DataFrame, days_roll_window: List[int]
) -> pd.DataFrame:

    idx = []
    new_df = pd.DataFrame()

    df = df.sort_values(by="date", ascending=True).reset_index(drop=True)

    _max_date = df["date"].max().date()
    _min_date = df["date"].min().date()
    diff_days_weekdays = np.busday_count(_min_date, _max_date)

    windows = days_roll_window + list(range(5, diff_days_weekdays, 5))

    threshold = df.index.max()
    windows = [window for window in windows if window <= threshold]

    df.index = df.index + 1

    for window in windows:
        print(f"Calculating {window} days return window")
        # verificar essa lógica, deveria ter dividido pelo valor inicial e não pelo final
        temp = (df.iloc[0, 1:] - df.iloc[window, 1:]) / (df.iloc[window, 1:])
        idx.append(str(window) + "_days_return")
        new_df = pd.concat([new_df, temp.to_frame().T], ignore_index=True)

    new_df.index = idx

    return new_df
