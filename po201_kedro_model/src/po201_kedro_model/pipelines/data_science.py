from kedro.pipeline import Pipeline, node, pipeline
from po201_kedro_model.data_domains.yahoo_finance import (
    yahoo_finance_primary,
    yahoo_finance_features,
)
from po201_kedro_model.models import model_run


def data_science_pipeline():

    yahoo_finance_pipeline = pipeline(
        Pipeline(
            [
                node(
                    func=yahoo_finance_primary,
                    inputs=[
                        "yf_hdfc_prm",
                        "yf_itc_prm",
                        "yf_l_and_t_prm",
                        "yf_m_and_m_prm",
                        "yf_sunpha_prm",
                        "yf_tcs_prm",
                    ],
                    outputs="yf_tickers_fte",
                    name="process_yahoo_finance_prm",
                ),
                node(
                    func=yahoo_finance_features,
                    inputs=["yf_tickers_fte", "params:month_roll_window"],
                    outputs="yf_tickers_mi",
                    name="process_yahoo_finance_fte",
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
                    ],
                    outputs="dummy",
                )
            ]
        )
    )

    return yahoo_finance_pipeline + generic_algorithm_pipeline
