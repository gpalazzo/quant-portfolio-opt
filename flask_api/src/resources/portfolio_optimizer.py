from flask_restful import Resource
from flask import request
from typing import Tuple, List, Dict, Any
from utils import dump_data_pgsql, read_data_pgsql, load_and_merge_ymls
import uuid
from datetime import datetime
import pandas as pd
import os
from flasgger.utils import swag_from
from pathlib import Path
import requests


# get the path to the root project directory
project_dir = Path(__file__).resolve().parents[2]


READ_AVAILABLE_TICKERS_ENDPOINT = "/available_tickers"
READ_RESULTS_ENDPOINT = "/optimization_results"
# reading configs from yml file
CONFIG_PATH = [f"{os.getenv('PROJECT_ROOT_PATH')}/conf/io.yml"]


class PortfolioOptimizer(Resource):
    """Class for requesting optimization"""

    def __init__(self):
        self.input = request.get_json().get(
            "tickers"
        )  # post call must have a json key named as `tickers`
        self.input_parsed = self._parse_input()
        self.available_tickers = self._get_available_tickers()
        self.uuid = uuid.uuid4()
        self.dump_df = None
        self.dump_status = None
        self.output = None
        self.post_code = None
        self.run()

    def _parse_input(self) -> List[str]:
        """Parse input from API call

        Returns:
            list of string with assets' names
        """

        tickers = [ticker.strip() for ticker in self.input.split(",")]
        return tickers

    @staticmethod
    def _get_available_tickers() -> List[str]:
        """Calls API endpoint for retrieving available tickers

        Returns:
            list of strings holding assets' names
        """

        # TODO: get API host dynamically
        avail_tickers_url = "http://localhost:5000/available_tickers"
        avail_tickers_r = requests.get(avail_tickers_url)
        return eval(avail_tickers_r.text)["available_stocks"]

    def run(self) -> None:
        """Runs the optimization request

        Returns:
            None, it changes class' state by updating attribute
        """

        input_diff = self._validate_input()

        # if != 0 it means there were requested more tickers than the
        # availability of the service
        if len(input_diff) != 0:
            self.dump_status = (
                f"input failed. please refer to {READ_AVAILABLE_TICKERS_ENDPOINT} "
                "endpoint to see available tickers."
            )

        else:
            self.dump_df = self._build_output_df()
            self.dump_status = self._dump_data()

        self.output = self._build_output()

    def _validate_input(self) -> List[str]:
        """Check differences in the available tickers and the tickers sent through the API

        Returns:
            list of strings with different assets. It there's no difference,
            the output will be an empty list `[]`
        """

        return list(set(self.input_parsed) - set(self.available_tickers))

    def _build_output_df(self) -> pd.DataFrame:
        """Builds output

        Returns:
            pandas dataframe with relevant data for the optimization request
        """

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

    def _dump_data(self) -> str:
        """Dumps data to PostgreSQL database

        Returns:
            string representing state of the data dump. It could be either `success`
            or the error arguments (if any)
        """

        try:
            dump_data_pgsql(
                df=self.dump_df, database="aux", tbl_name="optimizer_api_requests"
            )
            return "success"

        except Exception as e:
            return e.args

    def _build_output(self) -> Dict[str, str]:
        """Builds output for the final user

        Returns:
            dict of strings. Most important info is the `uuid`
        """

        if self.dump_status == "success":
            return {
                "optimization_status": "started",
                "results_endpoint": READ_RESULTS_ENDPOINT,
                "uuid": str(self.uuid),
                "error": "",
            }

        else:
            return {
                "optimization_status": "fail",
                "results_endpoint": "",
                "uuid": "",
                "error": self.dump_status,
            }

    @swag_from(
        f"{project_dir}/conf/endpoints/portfolio_optimize.yml"
    )  # parse swagger docs from file
    def post(self) -> Tuple[Dict[str, Any], int]:
        """Invoked when endpoint receives HTTP POST method
            If process was success, response code defaults to 201,
                otherwise it defaults to 500

        Returns:
            tuple of dict holding output and response code
        """

        if self.dump_status == "success":
            self.post_code = 201
        else:
            self.post_code = 500

        return self.output, self.post_code
