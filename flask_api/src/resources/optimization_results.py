from flask_restful import Resource
from flask import request
from typing import Tuple, Dict, Any
from utils import read_data_pgsql
import pandas as pd
from flasgger.utils import swag_from
from pathlib import Path


# get the path to the root project directory
project_dir = Path(__file__).resolve().parents[2]


class OptimizationResults(Resource):
    """Class for parsing optimization results"""

    def __init__(self):
        self.input = request.get_json().get(
            "uuid"
        )  # post call must have a json key named as `uuid`
        self._validate_input()
        self.query = self._build_query()
        self.data = self._read_data()
        self.output = self._build_output()

    def _validate_input(self) -> None:
        """Validate inputs to avoid both attacks and wrong input

        Returns:
            None, asserts an error instead
        """
        pass

    def _build_query(self) -> str:
        """Build query to retrieve appropriate data

        Returns:
            str representing SQL query
        """

        sql = f"select * from bl_report where uuid in ('{self.input}')"
        return sql

    def _read_data(self) -> pd.DataFrame:
        """Reads data from PostgreSQL database

        Returns:
            pandas dataframe holding data from query. If there's any error
            while querying, it returns an empty dataframe
        """

        try:
            df = read_data_pgsql(database="aux", query=self.query)
            return df

        except Exception:
            return pd.DataFrame()

    def _build_output(self) -> Dict[str, Any]:
        """Build output for HTTP POST method

        Returns:
            dict of strings to Any holding optimization status with results (if any)
        """

        # if dataframe is empty it means the optimization is still running
        if self.data.empty:
            return {
                "optimization_status": "running",
                "results": "",
                "uuid": self.input,
            }

        else:
            # if dataframe is not empty, then parse results from optimization
            _data = self.data.astype(str)
            _data = _data.drop(columns=["uuid"])

            return {
                "optimization_status": "finished",
                "results": _data.to_dict(orient="list"),
                "uuid": self.input,
            }

    @swag_from(
        f"{project_dir}/conf/endpoints/optimization_results.yml"
    )  # parse swagger docs from file
    def post(self) -> Tuple[Dict[str, Any], int]:
        """Invoked when endpoint receives HTTP POST method
            It defaults the response code to 201

        Returns:
            tuple holding optimization results dict and the response code
        """

        return self.output, 201
