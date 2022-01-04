from flask_restful import Resource
from utils import read_data_pgsql, load_and_merge_ymls
import os
from typing import Dict, List
from flasgger.utils import swag_from
from pathlib import Path


# get the path to the root project directory
project_dir = Path(__file__).resolve().parents[2]

# reading configs from yml file
CONFIG_PATH = [f"{os.getenv('PROJECT_ROOT_PATH')}/conf/io.yml"]


class AvailableTickers(Resource):
    @staticmethod
    @swag_from(
        f"{project_dir}/conf/endpoints/available_tickers.yml"
    )  # parse swagger docs from file
    def get() -> Dict[str, List[str]]:
        """Invoked when endpoint receives HTTP GET method
            Parses available tickers from Airflow metadata table

        Returns:
            dict of str and list of available tickers
        """

        config = load_and_merge_ymls(paths=CONFIG_PATH)

        df = read_data_pgsql(
            database=config["yf_raw_stock_metadata_db_name"],
            tbl_name=config["yf_raw_stock_metadata_tbl_name"],
        )

        # gets only successfully dumped tickers
        # this info comes from airflow metadata
        df = df[df["dump_status"] == "dumped"]

        return {"available_stocks": df["stock_names"].unique().tolist()}
