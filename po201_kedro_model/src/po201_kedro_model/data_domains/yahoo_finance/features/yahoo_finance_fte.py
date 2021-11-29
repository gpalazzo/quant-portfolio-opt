import pandas as pd
from typing import List
from datetime import timedelta, datetime


def yahoo_finance_features(
    df: pd.DataFrame,
    month_roll_window: List[int],
    days_lookback: int,
    null_pct_cut: float,
) -> pd.DataFrame:

    df_pre_processed = _fte_pre_processing(
        df=df, days_lookback=days_lookback, null_pct_cut=null_pct_cut
    )

    df_ftes = _calculate_rolling_windows(
        df=df_pre_processed, month_roll_window=month_roll_window
    )

    return df_ftes


def _fte_pre_processing(
    df: pd.DataFrame, days_lookback: int, null_pct_cut: float
) -> pd.DataFrame:

    lower_bound_date = datetime.today() - timedelta(days=days_lookback)

    # filter date
    df_filter_date = df[df["date"] >= lower_bound_date]

    # drop rows with date not being at beginning of month
    df_filter_bom = df_filter_date[df_filter_date["date"].dt.is_month_start]

    # filter null percentage
    _mask = df_filter_bom.isna().mean()
    df_filter_null = df_filter_bom.loc[:, _mask <= null_pct_cut]

    # input nulls
    #   get columns with null value
    null_cols = df_filter_null.columns[df_filter_null.isna().any()].tolist()

    #   input with linear interpolation
    for col in null_cols:
        df_filter_null[col] = df_filter_null[col].interpolate(method="linear")

    return df_filter_null


def _calculate_rolling_windows(
    df: pd.DataFrame, month_roll_window: List[int]
) -> pd.DataFrame:

    idx = []
    new_df = pd.DataFrame()

    for mon in month_roll_window:
        print(f"Calculating {mon} months return window")
        temp = (df.iloc[0, 1:] - df.iloc[mon, 1:]) / (df.iloc[mon, 1:])
        idx.append(str(mon) + "_mon_return")
        new_df = pd.concat([new_df, temp.to_frame().T], ignore_index=True)

    new_df.index = idx

    return new_df
