import pandas as pd
import numpy as np
from typing import Tuple


def bl_prior():
    pass


def bl_investors_view():
    pass


def bl_posterior():
    pass


def run_black_litterman(
    df: pd.DataFrame, df_requests: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:

    final_df = pd.DataFrame(columns=["uuid", "tickers", "weights"])

    df_pending = df_requests[df_requests["status"] == "pending"]

    for uuid in df_pending["uuid"].unique().tolist():

        df_aux = df[df["uuid"] == uuid]

        """
        due to the append method in previous step, there might be tickers with 
        all values null in a column. it means that ticker must not be consider for 
        optimization in the given uuid
        """
        df_dropped = df_aux.dropna(axis=1, how="all")

        df_bl_weights = _calculate_bl_weights(df=df_dropped)

        final_df = final_df.append(df_bl_weights)

    df_requests.loc[:, "status"] = "done"

    return final_df, df_requests


def _calculate_bl_weights(df: pd.DataFrame) -> pd.DataFrame:

    tickers = df.set_index("uuid").columns.tolist()

    uuid = (
        df["uuid"].unique().tolist()[0]
    )  # assuming there's only uuid for optimization

    weights = np.random.random(size=len(tickers))

    df_weights = pd.DataFrame.from_dict(
        {"uuid": uuid, "tickers": tickers, "weights": weights}
    )

    return df_weights
