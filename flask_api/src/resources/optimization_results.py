from flask_restful import Resource
from flask import request
from typing import Tuple, Dict, Any
from utils import read_data_pgsql
import pandas as pd


class OptimizationResults(Resource):
    def __init__(self):
        self.input = request.get_json().get("uuid")
        self._validate_input()
        self.query = self._build_query()
        self.data = self._read_data()
        self.output = self._build_output()

    def _validate_input(self):
        pass

    def _build_query(self):
        sql = f"select * from bl_report where uuid in ('{self.input}')"
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
                "results": "",
                "uuid": self.input,
            }

        else:
            _data = self.data.astype(str)
            _data = _data.drop(columns=["uuid"])

            return {
                "optimization_status": "finished",
                "results": _data.to_dict(orient="list"),
                "uuid": self.input,
            }

    def post(self) -> Tuple[Dict[str, Any], int]:
        return self.output, 201
