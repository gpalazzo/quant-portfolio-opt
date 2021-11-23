import pandas as pd
from typing import List


def yahoo_finance_features(
    df: pd.DataFrame, month_roll_window: List[int]
) -> pd.DataFrame:

    df = _calculate_rolling_windows(df=df, month_roll_window=month_roll_window)

    return df


def _calculate_rolling_windows(
    df: pd.DataFrame, month_roll_window: List[int]
) -> pd.DataFrame:

    idx = []
    new_df = pd.DataFrame()

    for mon in month_roll_window:
        temp = (df.iloc[0, 1:] - df.iloc[mon, 1:]) / (df.iloc[mon, 1:])
        idx.append(str(mon) + "_mon_return")
        new_df = pd.concat([new_df, temp.to_frame().T], ignore_index=True)

    new_df.index = idx

    return new_df
