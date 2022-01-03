import pandas as pd
import requests
from typing import List
from utils import dump_data_pgsql, load_and_merge_ymls
import os


CONFIG_PATH = [f"{os.getenv('PROJECT_ROOT_PATH')}/conf/yahoo_finance/io.yml"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
}


def run_stock_names_raw():
    config = load_and_merge_ymls(paths=CONFIG_PATH)

    all_stocks = _get_all_stocks_b3()

    df = pd.DataFrame({"stocks_name": all_stocks})

    df = df.iloc[:50, :]

    dump_data_pgsql(
        df=df,
        database=config["yf_stock_names_db_name"],
        tbl_name=config["yf_stock_names_tbl_name"],
    )


def _get_all_stocks_b3() -> List[str]:

    response = requests.get(
        "https://www.fundamentus.com.br/detalhes.php?papel=",
        headers=HEADERS,
        verify=False,
    )

    df = pd.read_html(response.text)[0]

    stocks = [f"{stock}.SA" for stock in df["Papel"].unique().tolist()]

    return stocks
