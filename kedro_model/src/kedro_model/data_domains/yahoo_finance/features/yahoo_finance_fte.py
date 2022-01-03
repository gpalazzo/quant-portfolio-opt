import pandas as pd
from datetime import timedelta, datetime


def yahoo_finance_features(
    df_opt_requests: pd.DataFrame,
    df: pd.DataFrame,
    days_lookback: int,
    null_pct_cut: float,
) -> pd.DataFrame:

    final_df = pd.DataFrame()

    df_pending = df_opt_requests[df_opt_requests["status"] == "pending"]

    for uuid in df_pending["uuid"].unique().tolist():

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

        df_pre_processed.loc[:, "uuid"] = uuid

        final_df = final_df.append(df_pre_processed)

    return final_df


def yf_select_mktcap_tickers(
    df_stocks_mktcap: pd.DataFrame, yf_ticker_prices: pd.DataFrame
) -> pd.DataFrame:

    final_df = pd.DataFrame()

    yf_ticker_prices = yf_ticker_prices.drop(columns=["date"])

    for uuid in yf_ticker_prices["uuid"].unique().tolist():

        df_aux = yf_ticker_prices[yf_ticker_prices["uuid"] == uuid].drop(
            columns=["uuid"]
        )

        """
        due to the append method in previous step, there might be tickers with 
        all values null in a column. it means that ticker must not be consider for 
        optimization in the given uuid
        """
        df_dropped = df_aux.dropna(axis=1, how="all")
        tickers = df_dropped.columns.tolist()

        df_filtered = df_stocks_mktcap[df_stocks_mktcap["stocks"].isin(tickers)]

        df_filtered.loc[:, "uuid"] = uuid

        final_df = final_df.append(df_filtered)

    return final_df


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
