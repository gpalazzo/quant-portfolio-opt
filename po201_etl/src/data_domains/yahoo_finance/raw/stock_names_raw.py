import pandas as pd
import requests
from typing import List
from utils import dump_data_pgsql, load_and_merge_ymls
import os


CONFIG_PATH = [f"{os.getenv('PROJECT_ROOT_PATH')}/conf/yahoo_finance/io.yml"]
# considering IBXX index as of 2021-11-29
IBXX_STOCKS_INDEX = [
    "ALPA4.SA",
    "ABEV3.SA",
    "AMER3.SA",
    "ASAI3.SA",
    "AZUL4.SA",
    "B3SA3.SA",
    "BIDI4.SA",
    "BIDI11.SA",
    "BPAN4.SA",
    "BBSE3.SA",
    "BRML3.SA",
    "BBDC3.SA",
    "BBDC4.SA",
    "BRAP4.SA",
    "BBAS3.SA",
    "BRKM5.SA",
    "BRFS3.SA",
    "BPAC11.SA",
    "CRFB3.SA",
    "CCRO3.SA",
    "CMIG4.SA",
    "CESP6.SA",
    "CIEL3.SA",
    "COGN3.SA",
    "CPLE6.SA",
    "CSAN3.SA",
    "CPFE3.SA",
    "CVCB3.SA",
    "CYRE3.SA",
    "DXCO3.SA",
    "ECOR3.SA",
    "ELET3.SA",
    "ELET6.SA",
    "EMBR3.SA",
    "ENBR3.SA",
    "ENGI11.SA",
    "ENEV3.SA",
    "EGIE3.SA",
    "EQTL3.SA",
    "EZTC3.SA",
    "FLRY3.SA",
    "GGBR4.SA",
    "GOAU4.SA",
    "GETT11.SA",
    "GOLL4.SA",
    "NTCO3.SA",
    "SOMA3.SA",
    "HAPV3.SA",
    "HYPE3.SA",
    "IGTI11.SA",
    "GNDI3.SA",
    "IRBR3.SA",
    "ITSA4.SA",
    "ITUB4.SA",
    "JBSS3.SA",
    "JHSF3.SA",
    "KLBN11.SA",
    "LIGT3.SA",
    "RENT3.SA",
    "LCAM3.SA",
    "LWSA3.SA",
    "LAME3.SA",
    "LAME4.SA",
    "LREN3.SA",
    "MGLU3.SA",
    "MRFG3.SA",
    "CASH3.SA",
    "BEEF3.SA",
    "MOVI3.SA",
    "MRVE3.SA",
    "MULT3.SA",
    "PCAR3.SA",
    "PETR3.SA",
    "PETR4.SA",
    "PRIO3.SA",
    "PETZ3.SA",
    "PSSA3.SA",
    "POSI3.SA",
    "QUAL3.SA",
    "RADL3.SA",
    "RAPT4.SA",
    "RDOR3.SA",
    "RAIL3.SA",
    "SBSP3.SA",
    "SAPR11.SA",
    "SANB11.SA",
    "CSNA3.SA",
    "SULA11.SA",
    "SUZB3.SA",
    "TAEE11.SA",
    "TASA4.SA",
    "VIVT3.SA",
    "TIMS3.SA",
    "TOTS3.SA",
    "UGPA3.SA",
    "USIM5.SA",
    "VALE3.SA",
    "VIIA3.SA",
    "VBBR3.SA",
    "WEGE3.SA",
    "YDUQ3.SA",
]


def run_stock_names_raw():
    config = load_and_merge_ymls(paths=CONFIG_PATH)

    priority_stocks = {}
    prioritized_stocks = _get_prioritized_stocks()

    for ibxx_stock in IBXX_STOCKS_INDEX:
        if ibxx_stock in prioritized_stocks:
            priority_stocks[ibxx_stock] = "yes"
        else:
            priority_stocks[ibxx_stock] = "no"

    df = pd.DataFrame(
        {"stocks_name": priority_stocks.keys(), "priority": priority_stocks.values()}
    )

    dump_data_pgsql(
        df=df,
        database=config["yf_stock_names_db_name"],
        tbl_name=config["yf_stock_names_tbl_name"],
    )


def _get_prioritized_stocks(target_index: str = "IBXX.SA") -> List[str]:
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
