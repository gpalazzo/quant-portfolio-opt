from flask_restful import Resource
from flask import request
from typing import Tuple, List
import uuid


class PortfolioOptimizer(Resource):
    def __init__(self):
        self.input = request.get_json().get("tickers")
        self.input_parsed = self._parse_input()
        self.output = self._build_output()

    def post(self) -> Tuple[List[str], int]:
        return self.output, 201

    def _parse_input(self) -> List[str]:
        """
        Private method to handle the HTTP POST method in the API and apply data type adjustments

        Returns:
            list of user_ids as integer data type
        """

        tickers = [ticker.strip() for ticker in self.input.split(",")]
        return tickers

    def _build_output(self):
        return self.input_parsed
