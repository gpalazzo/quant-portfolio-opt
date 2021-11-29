import pandas as pd
import requests
from typing import List
from utils import dump_data_pgsql, load_and_merge_ymls
import os


CONFIG_PATH = [f"{os.getenv('PROJECT_ROOT_PATH')}/conf/yahoo_finance/io.yml"]


def run_stock_names_raw():
    config = load_and_merge_ymls(paths=CONFIG_PATH)
    stocks = _parse_stocks_index()
    df = pd.DataFrame({"stocks_name": stocks})
    dump_data_pgsql(
        df=df,
        database=config["yf_stock_names_db_name"],
        tbl_name=config["yf_stock_names_tbl_name"],
    )


def _parse_stocks_index(target_index: str = "IBXX.SA") -> List[str]:
    """This function uses the `IBXX.SA` index only to find the companies within IBXX

    Args:
        target_index:

    Returns:

    """

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    }
    response = requests.get(
        f"https://finance.yahoo.com/quote/{target_index}/components?p={target_index}",
        headers=headers,
        verify=False,
    )

    df = pd.read_html(response.text)[0]

    return list(set(df["Symbol"]))
