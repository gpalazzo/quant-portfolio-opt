from flask_restful import Resource
from flask import request
from typing import Tuple, List, Dict, Any
from utils import read_data_pgsql
import pandas as pd


TABLE_NAME = "optimizer_api_requests"


class OptimizationResults(Resource):
    def __init__(self):
        self.input = request.get_json().get("uuid")
        self.input_parsed = self._parse_input()
        self._validate_input()
        self.query = self._build_query()
        self.data = self._read_data()
        # self.output = self.query
        self.output = self._build_output()

    def _parse_input(self) -> List[str]:
        tickers = [ticker.strip() for ticker in self.input.split(",")]
        return tickers

    def _validate_input(self):
        pass

    def _build_query(self):
        sql = f"select * from optimizer_api_requests where uuid in ('{self.input}')"
        return sql

    def _read_data(self):
        try:
            df = read_data_pgsql(database="aux", query=self.query)
            return df

        except Exception:
            return pd.DataFrame()

    def _build_output(self):
        if self.data.empty:
            return {
                "optimization_status": "running",
                "results": None,
                "uuid": self.input,
            }

        else:
            # aqui faz o parsing do output que vai sair do Kedro
            _data = self.data.astype(str)

            return {
                "optimization_status": "finished",
                "results": _data.to_dict(),
                "uuid": self.input,
            }

    def post(self) -> Tuple[Dict[str, Any], int]:
        return self.output, 201
