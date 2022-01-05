import pandas as pd
import numpy as np
from typing import Tuple
from pypfopt import (
    black_litterman,
    risk_models,
    BlackLittermanModel,
    EfficientFrontier,
    objective_functions,
)


def bl_prior(
    df_prices: pd.DataFrame, df_mktcap: pd.DataFrame, df_requests: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Applies Black-Litterman (BL) prior stage

    Args:
        df_prices: pandas dataframe with adjusted close prices for stocks
        df_mktcap: pandas dataframe with market capitalization value for stocks
        df_requests: pandas dataframe with requests coming from the API

    Returns:
        tuple of pandas dataframes with market prior values of BL model and price covariance
    """

    final_df = pd.DataFrame()
    cov_df = pd.DataFrame()

    # filter only pending requests for the API
    df_pending = df_requests[df_requests["status"] == "pending"]

    for uuid in df_pending["uuid"].unique().tolist():

        mktcap_dict = {}

        df_aux_mktcap = df_mktcap[df_mktcap["uuid"] == uuid].drop(columns=["uuid"])

        # parsing market capitalization to dict format as BL method is expecting
        for mktcap_data in df_aux_mktcap.to_dict(orient="split")["data"]:
            mktcap_dict[mktcap_data[0]] = mktcap_data[1]

        df_aux_prices = df_prices[df_prices["uuid"] == uuid].drop(columns=["uuid"])

        # build data structure only with market index
        df_aux_index = df_aux_prices[["date", "bvsp"]].set_index("date")
        # build data structure only with stocks close price
        df_aux_prices = df_aux_prices[["date"] + list(mktcap_dict.keys())].set_index(
            "date"
        )

        # covariance of prices
        S = risk_models.CovarianceShrinkage(df_aux_prices).ledoit_wolf()
        # market risk aversion parameter calculated with index
        delta = black_litterman.market_implied_risk_aversion(df_aux_index)
        # calculate market prior
        market_prior = black_litterman.market_implied_prior_returns(
            mktcap_dict, float(delta), S
        )

        S.loc[:, "uuid"] = uuid

        df = (
            pd.DataFrame(market_prior, columns=["market_prior"])
            .reset_index()
            .rename(columns={"index": "tickers"})
        )
        df.loc[:, "uuid"] = uuid

        final_df = final_df.append(df)
        cov_df = cov_df.append(S)

    return final_df, cov_df


def bl_investors_view(
    df_prior: pd.DataFrame, df_requests: pd.DataFrame
) -> pd.DataFrame:
    """Applies Black-Litterman (BL) investor's view stage

    Args:
        df_prior: pandas dataframe with results from BL prior stage
        df_requests: pandas dataframe with requests coming from the API

    Returns:
        pandas dataframe with Investor's View results
    """

    final_df = pd.DataFrame()

    # filter only pending requests for the API
    df_pending = df_requests[df_requests["status"] == "pending"]

    for uuid in df_pending["uuid"].unique().tolist():

        view_dict = {}
        confidence = []

        df_aux = df_prior[df_prior["uuid"] == uuid].drop(columns=["uuid"])

        for ticker in df_aux["tickers"].unique().tolist():
            view_dict[ticker] = np.random.random()
            confidence.append(np.random.random())

        df_investors_view = pd.DataFrame(
            {
                "stocks": list(view_dict.keys()),
                "expected_growth": list(view_dict.values()),
                "confidence": confidence,
            }
        )
        df_investors_view.loc[:, "uuid"] = uuid

        final_df = final_df.append(df_investors_view)

    return final_df


def bl_posterior(
    df_prior: pd.DataFrame,
    df_investors_view: pd.DataFrame,
    df_cov_prices: pd.DataFrame,
    df_requests: pd.DataFrame,
) -> pd.DataFrame:
    """Applies Black-Litterman (BL) posterior stage

    Args:
        df_prior: pandas dataframe with results from BL prior stage
        df_investors_view: pandas dataframe with results from BL investor's view
        df_cov_prices: pandas dataframe with price covariance from BL prior stage
        df_requests: pandas dataframe with requests coming from the API

    Returns:
        pandas dataframe with stocks and their respective weights for each request uuid
    """

    final_df = pd.DataFrame()

    # filter only pending requests for the API
    df_pending = df_requests[df_requests["status"] == "pending"]

    for uuid in df_pending["uuid"].unique().tolist():

        df_investors_view_aux = df_investors_view[df_investors_view["uuid"] == uuid]
        market_prior = (
            df_prior[df_prior["uuid"] == uuid]
            .drop(columns=["uuid"])
            .set_index("tickers")
        )
        df_cov_prices_aux = df_cov_prices[df_cov_prices["uuid"] == uuid].drop(
            columns=["uuid"]
        )

        """
        due to the append method in previous step, there might be tickers with 
        all values null in a column. it means that ticker must not be consider for 
        optimization in the given uuid
        """
        df_cov_prices_aux = df_cov_prices_aux.dropna(axis=1, how="all")
        # rebuild index of covariance dataframe as it was lost during saving process
        df_cov_prices_aux.index = df_cov_prices_aux.columns.tolist()

        view_dict = {}
        for investors_view in df_investors_view_aux.to_dict(orient="split")["data"]:
            view_dict[investors_view[0]] = investors_view[1]
        confidence = df_investors_view_aux["confidence"].tolist()

        # build BL model
        bl = BlackLittermanModel(
            df_cov_prices_aux,
            pi=market_prior,
            absolute_views=view_dict,
            omega="idzorek",
            view_confidences=confidence,
        )

        # get BL returns
        bl_ret = bl.bl_returns()
        # get BL covariance
        bl_covar = bl.bl_cov()

        # calculate weights by maximizing sharpe ratio
        ef = EfficientFrontier(bl_ret, bl_covar)
        ef.add_objective(objective_functions.L2_reg)
        ef.max_sharpe()
        weights = dict(ef.clean_weights())

        try:
            staging_df = pd.DataFrame(
                {
                    "uuid": uuid,
                    "tickers": list(weights.keys()),
                    "weights": list(weights.values()),
                }
            )
        except:
            staging_df = pd.DataFrame(
                {
                    "uuid": uuid,
                    "tickers": list(weights.keys()),
                    "weights": list(weights.values()),
                },
                index=[0],
            )

        final_df = final_df.append(staging_df)

    return final_df


def bl_final_parser(
    df_posterior: pd.DataFrame, df_requests: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Parsing final values of API requests' table

    Args:
        df_posterior: pandas dataframe with BL posterior values
        df_requests: pandas dataframe with requests coming from the API

    Returns:
        tuple of pandas dataframe with BL final values and updated API requests' table
    """

    # update API requests' table with status `done`
    for uuid in df_posterior["uuid"].unique().tolist():
        df_requests.loc[df_requests["uuid"] == uuid, "status"] = "done"

    return df_posterior, df_requests
