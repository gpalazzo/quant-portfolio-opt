from flask_restful import Resource
from utils import read_data_pgsql, load_and_merge_ymls
import os
from typing import Dict, List


CONFIG_PATH = [f"{os.getenv('PROJECT_ROOT_PATH')}/conf/io.yml"]


class AvailableTickers(Resource):
    @staticmethod
    def get() -> Dict[str, List[str]]:
        config = load_and_merge_ymls(paths=CONFIG_PATH)

        df = read_data_pgsql(
            database=config["yf_raw_stock_metadata_db_name"],
            tbl_name=config["yf_raw_stock_metadata_tbl_name"],
        )

        df = df[df["dump_status"] == "dumped"]

        return {"available_stocks": df["stock_names"].unique().tolist()}
