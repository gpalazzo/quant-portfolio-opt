import pandas as pd
import requests
from typing import List
from utils import dump_data_pgsql, load_and_merge_ymls
import os


# reading configs from yml file
CONFIG_PATH = [f"{os.getenv('PROJECT_ROOT_PATH')}/conf/yahoo_finance/io.yml"]

# headers for web scrapping
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
}


def run_stock_names_raw() -> None:
    """Load, parse and dump all stocks listed in B3

    Returns:
        None, it dumps data to a PostgreSQL table instead
    """

    config = load_and_merge_ymls(paths=CONFIG_PATH)

    all_stocks = _get_all_stocks_b3()

    df = pd.DataFrame({"stocks_name": all_stocks})

    # parsing the first 100 stocks to accelerate the data dumping process and tests
    df = df.iloc[:100, :]

    dump_data_pgsql(
        df=df,
        database=config["yf_stock_names_db_name"],
        tbl_name=config["yf_stock_names_tbl_name"],
    )


def _get_all_stocks_b3() -> List[str]:
    """Get all stocks listed in B3
    It adds the suffix `.SA` to the name for parity with yahoo finance stock names

    Returns:
        list of strings with stock names
    """

    response = requests.get(
        "https://www.fundamentus.com.br/detalhes.php?papel=",
        headers=HEADERS,
        verify=False,
    )

    df = pd.read_html(response.text)[0]

    stocks = [f"{stock}.SA" for stock in df["Papel"].unique().tolist()]

    return stocks
