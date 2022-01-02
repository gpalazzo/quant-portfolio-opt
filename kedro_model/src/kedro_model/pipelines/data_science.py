from kedro.pipeline import Pipeline, node, pipeline
from kedro_model.data_domains.yahoo_finance import (
    yahoo_finance_features,
    yf_select_mktcap_tickers,
)
from kedro_model.models import run_black_litterman


def data_science_pipeline():

    yahoo_finance_pipeline = pipeline(
        Pipeline(
            [
                node(
                    func=yahoo_finance_features,
                    inputs=[
                        "api_optimizing_requests",
                        "yf_tickers_fte",
                        "params:days_roll_window",
                        "params:days_lookback",
                        "params:null_pct_cut",
                    ],
                    outputs="yf_tickers_mi",
                    name="process_yahoo_finance_fte",
                ),
                node(
                    func=yf_select_mktcap_tickers,
                    inputs=["yf_tickers_mktcap_fte", "yf_tickers_mi"],
                    outputs="yf_tickers_mktcap_mi",
                    name="process_yf_stocks_mktcap",
                ),
            ],
            tags=["yahoo_finance"],
        )
    )

    black_litterman_pipeline = pipeline(
        Pipeline(
            [
                node(
                    func=run_black_litterman,
                    inputs=["yf_tickers_mi", "api_optimizing_requests"],
                    outputs=["model_results", "api_optimizing_requests_update"],
                    name="process_bl_model",
                )
            ],
            tags=["bl_model"],
        )
    )

    return yahoo_finance_pipeline + black_litterman_pipeline
