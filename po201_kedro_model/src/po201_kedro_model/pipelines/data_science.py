from kedro.pipeline import Pipeline, node, pipeline
from po201_kedro_model.data_domains.yahoo_finance import (
    yahoo_finance_features,
    yf_select_mktcap_tickers,
)
from po201_kedro_model.models import model_run


def data_science_pipeline():

    yahoo_finance_pipeline = pipeline(
        Pipeline(
            [
                node(
                    func=yahoo_finance_features,
                    inputs=[
                        "yf_tickers_fte",
                        "yf_ticker_names_priorities",
                        "params:month_roll_window",
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

    generic_algorithm_pipeline = pipeline(
        Pipeline(
            [
                node(
                    func=model_run,
                    inputs=[
                        "yf_tickers_mi",
                        "params:qty_stocks",
                        "params:population_size",
                        "params:risk_free_rate",
                        "params:qty_iterations",
                        "params:max_expected_return",
                        "params:min_expected_risk",
                    ],
                    outputs="dummy",
                    name="process_ga_model",
                )
            ],
            tags=["ga_model"],
        )
    )

    return yahoo_finance_pipeline + generic_algorithm_pipeline
