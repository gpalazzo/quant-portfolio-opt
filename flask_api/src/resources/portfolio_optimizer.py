from flask_restful import Resource
from flask import request
from typing import Tuple, List, Dict, Any
from utils import dump_data_pgsql, read_data_pgsql, load_and_merge_ymls
import uuid
from datetime import datetime
import pandas as pd
import os


READ_AVAILABLE_TICKERS_ENDPOINT = "/available_tickers"
READ_RESULTS_ENDPOINT = "/optimization_results"
CONFIG_PATH = [f"{os.getenv('PROJECT_ROOT_PATH')}/conf/io.yml"]


class PortfolioOptimizer(Resource):
    def __init__(self):
        self.input = request.get_json().get("tickers")
        self.input_parsed = self._parse_input()
        self.available_tickers = self._get_available_tickers()
        self.uuid = uuid.uuid4()
        self.dump_df = None
        self.dump_status = None
        self.output = None
        self.post_code = None
        self.run()

    def _parse_input(self) -> List[str]:
        tickers = [ticker.strip() for ticker in self.input.split(",")]
        return tickers

    @staticmethod
    def _get_available_tickers() -> List[str]:
        # TODO: fazer essa chamada usando o endpoint de Available Tickers
        config = load_and_merge_ymls(paths=CONFIG_PATH)
        df = read_data_pgsql(
            database=config["yf_raw_stock_metadata_db_name"],
            tbl_name=config["yf_raw_stock_metadata_tbl_name"],
        )

        df = df[df["dump_status"] == "dumped"]

        return df["stock_names"].unique().tolist()

    def run(self):
        input_diff = self._validate_input()

        if len(input_diff) != 0:
            self.dump_status = (
                f"input failed. please refer to {READ_AVAILABLE_TICKERS_ENDPOINT} "
                "endpoint to see available tickers."
            )

        else:
            self.dump_df = self._build_output_df()
            self.dump_status = self._dump_data()

        self.output = self._build_output()

    def _validate_input(self):
        return list(set(self.input_parsed) - set(self.available_tickers))

    def _build_output_df(self):
        _now = datetime.now()
        status = "pending"

        return pd.DataFrame(
            {
                "uuid": self.uuid,
                "request_time": _now,
                "status": status,
                "tickers": self.input,
            },
            index=[0],
        )

    def _dump_data(self):
        try:
            dump_data_pgsql(
                df=self.dump_df, database="aux", tbl_name="optimizer_api_requests"
            )
            return "success"

        except Exception as e:
            return e.args

    def _build_output(self):
        if self.dump_status == "success":
            return {
                "optimization_status": "started",
                "results_endpoint": READ_RESULTS_ENDPOINT,
                "uuid": str(self.uuid),
                "error": None,
            }

        else:
            return {
                "optimization_status": "fail",
                "results_endpoint": None,
                "uuid": None,
                "error": self.dump_status,
            }

    def post(self) -> Tuple[Dict[str, Any], int]:
        if self.dump_status == "success":
            self.post_code = 201
        else:
            self.post_code = 500

        return self.output, self.post_code
