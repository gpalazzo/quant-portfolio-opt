from flask_restful import Resource
from flask import request
from typing import Tuple, List, Dict, Any
from utils import dump_data_pgsql
import uuid
from datetime import datetime
import pandas as pd


READ_RESULTS_ENDPOINT = "abc"


class PortfolioOptimizer(Resource):
    def __init__(self):
        self.input = request.get_json().get("tickers")
        self.input_parsed = self._parse_input()
        self._validate_input()
        self.uuid = uuid.uuid4()
        self.dump_df = self._build_output_df()
        self.dump_status = self._dump_data()
        self.output = self._build_output()

    def _parse_input(self) -> List[str]:
        tickers = [ticker.strip() for ticker in self.input.split(",")]
        return tickers

    def _validate_input(self):
        pass

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
        return self.output, 201
