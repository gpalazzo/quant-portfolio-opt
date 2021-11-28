from utils import dump_data_pgsql, read_data_pgsql, load_and_merge_ymls
import os


CONFIG_PATH = [f"{os.getenv('PROJECT_ROOT_PATH')}/conf/yahoo_finance/io.yml"]
config = load_and_merge_ymls(paths=CONFIG_PATH)

df = read_data_pgsql(
    database=config["yf_int_db_name"], tbl_name=config["yf_int_tbl_name"]
)

df.columns = [col.lower().replace(".sa", "") for col in df.columns]

dump_data_pgsql(
    df=df, database=config["yf_prm_db_name"], tbl_name=config["yf_prm_tbl_name"]
)
