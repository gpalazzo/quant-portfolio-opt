from kedro.pipeline import Pipeline, node, pipeline
from po201_kedro_model.data_domains.yahoo_finance import (
    yahoo_finance_features,
    yahoo_finance_features_aux,
)


def data_science_pipeline():

    yahoo_finance_pipeline = pipeline(
        Pipeline(
            [
                node(
                    func=yahoo_finance_features,
                    inputs=["tickers_table_fte"],
                    outputs=["tickers_table_mi"],
                    name="process_yahoo_finance_fte",
                ),
                node(
                    func=yahoo_finance_features_aux,
                    inputs=["tickers_table_mi"],
                    outputs=["tickers_table_mi2"],
                    name="process_yahoo_finance_fte_aux",
                ),
            ],
            tags=["yahoo_finance"],
        )
    )

    return yahoo_finance_pipeline
