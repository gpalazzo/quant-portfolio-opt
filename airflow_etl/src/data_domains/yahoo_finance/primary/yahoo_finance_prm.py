from utils import dump_data_pgsql, read_data_pgsql, load_and_merge_ymls
import os


# reading configs from yml file
CONFIG_PATH = [f"{os.getenv('PROJECT_ROOT_PATH')}/conf/yahoo_finance/io.yml"]
config = load_and_merge_ymls(paths=CONFIG_PATH)


def run_yf_stock_prices_primary() -> None:
    """Load, parse and dump stock price data

    Returns:
        None, it dumps data to a PostgreSQL table instead
    """

    df = read_data_pgsql(
        database=config["yf_int_stock_prices_db_name"],
        tbl_name=config["yf_int_stock_prices_tbl_name"],
    )

    # rename columns
    df.columns = [col.lower().replace(".sa", "").replace("^", "") for col in df.columns]

    dump_data_pgsql(
        df=df,
        database=config["yf_prm_stock_prices_db_name"],
        tbl_name=config["yf_prm_stock_prices_tbl_name"],
    )


def run_yf_mktcap_primary() -> None:
    """Load, parse and dump market capitalization data

    Returns:
        None, it dumps data to a PostgreSQL table instead
    """

    df = read_data_pgsql(
        database=config["yf_int_stock_mktcap_db_name"],
        tbl_name=config["yf_int_stock_mktcap_tbl_name"],
    )

    # drop unused columns
    df = df.drop(columns=["status"])

    cols = df.select_dtypes(include=[object]).columns

    # rename columns
    for col in cols:
        df[col] = df[col].str.lower().str.replace(".sa", "")

    dump_data_pgsql(
        df=df,
        database=config["yf_prm_stock_mktcap_db_name"],
        tbl_name=config["yf_prm_stock_mktcap_tbl_name"],
    )
