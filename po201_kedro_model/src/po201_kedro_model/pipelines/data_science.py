from kedro.pipeline import Pipeline, node, pipeline
from po201_kedro_model.data_domains.yahoo_finance import yahoo_finance_features


def data_science_pipeline():

    yahoo_finance_pipeline = pipeline(
        Pipeline(
            [
                node(
                    func=yahoo_finance_features,
                    inputs=[""],
                    outputs=[""],
                    name="process_yahoo_finance_fte",
                )
            ],
            tags=["yahoo_finance"],
        )
    )

    return yahoo_finance_pipeline
