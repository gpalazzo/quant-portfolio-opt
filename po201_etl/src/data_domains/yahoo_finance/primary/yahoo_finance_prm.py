from utils import dump_data_pgsql, read_data_pgsql, load_and_merge_ymls
import os


CONFIG_PATH = [f"{os.getenv('PROJECT_ROOT_PATH')}/conf/yahoo_finance/io.yml"]
config = load_and_merge_ymls(paths=CONFIG_PATH)


def run_yf_stock_prices_primary():

    df = read_data_pgsql(
        database=config["yf_int_stock_prices_db_name"],
        tbl_name=config["yf_int_stock_prices_tbl_name"],
    )

    df.columns = [col.lower().replace(".sa", "") for col in df.columns]

    dump_data_pgsql(
        df=df,
        database=config["yf_prm_stock_prices_db_name"],
        tbl_name=config["yf_prm_stock_prices_tbl_name"],
    )


def run_yf_mktcap_primary():

    df = read_data_pgsql(
        database=config["yf_int_stock_mktcap_db_name"],
        tbl_name=config["yf_int_stock_mktcap_tbl_name"],
    )

    cols = df.select_dtypes(include=[object]).columns

    for col in cols:
        df[col] = df[col].str.lower().str.replace(".sa", "")

    dump_data_pgsql(
        df=df,
        database=config["yf_prm_stock_mktcap_db_name"],
        tbl_name=config["yf_prm_stock_mktcap_tbl_name"],
    )
