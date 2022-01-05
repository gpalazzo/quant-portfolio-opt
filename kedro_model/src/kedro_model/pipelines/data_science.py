from kedro.pipeline import Pipeline, node, pipeline
from kedro_model.data_domains.yahoo_finance import (
    yahoo_finance_features,
    yf_select_mktcap_tickers,
)
from kedro_model.models import (
    bl_final_parser,
    bl_prior,
    bl_investors_view,
    bl_posterior,
)


def data_science_pipeline():

    # yahoo finance pipeline
    yahoo_finance_pipeline = pipeline(
        Pipeline(
            [
                node(
                    func=yahoo_finance_features,
                    inputs=[
                        "api_optimizing_requests",
                        "yf_tickers_fte",
                        "params:days_lookback",
                        "params:null_pct_cut",
                    ],
                    outputs="yf_ticker_prices_mi",
                    name="process_yahoo_finance_fte",
                ),
                node(
                    func=yf_select_mktcap_tickers,
                    inputs=[
                        "yf_tickers_mktcap_fte",
                        "yf_ticker_prices_mi",
                    ],
                    outputs="yf_ticker_mktcap_mi",
                    name="process_yf_stocks_mktcap",
                ),
            ],
            tags=["yahoo_finance"],
        )
    )

    # black-litterman model pipeline
    black_litterman_pipeline = pipeline(
        Pipeline(
            [
                node(
                    func=bl_prior,
                    inputs=[
                        "yf_ticker_prices_mi",
                        "yf_ticker_mktcap_mi",
                        "api_optimizing_requests",
                    ],
                    outputs=["bl_prior", "bl_cov_prices"],
                    name="process_bl_prior",
                ),
                node(
                    func=bl_investors_view,
                    inputs=["bl_prior", "api_optimizing_requests"],
                    outputs="bl_investors_view",
                    name="process_bl_investors_view",
                ),
                node(
                    func=bl_posterior,
                    inputs=[
                        "bl_prior",
                        "bl_investors_view",
                        "bl_cov_prices",
                        "api_optimizing_requests",
                    ],
                    outputs="bl_posterior",
                    name="process_bl_posterior",
                ),
                node(
                    func=bl_final_parser,
                    inputs=["bl_posterior", "api_optimizing_requests"],
                    outputs=["model_results", "api_optimizing_requests_update"],
                    name="process_bl_parser",
                ),
            ],
            tags=["bl_model"],
        )
    )

    return yahoo_finance_pipeline + black_litterman_pipeline
