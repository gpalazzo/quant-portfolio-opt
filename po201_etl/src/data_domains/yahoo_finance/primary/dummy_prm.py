# from pathlib import Path
# import yaml
# from utils import read_data_file, dump_data_file, camelcase_to_snakecase
# from data_domains.schemas import date_time_prm_schema
# import numpy as np
#
#
# root_path = Path(__file__).resolve().parents[4]
#
#
def dummy_primary() -> None:
    print("hello")
#     with open(f"{root_path}/conf/date_time.yml") as f:
#         conf = yaml.load(f, Loader=yaml.FullLoader)
#
#     for read_file_name, read_file_type, dump_file_name, dump_file_type in zip(
#         *[
#             conf["date_time_file_name_prm"],
#             conf["date_time_file_type_prm"],
#             conf["date_time_file_name_fte"],
#             conf["date_time_file_type_fte"],
#         ]
#     ):
#
#         # read
#         df = read_data_file(
#             read_base_path=conf["date_time_base_path_prm"],
#             file_name=read_file_name,
#             file_type=read_file_type,
#         )
#
#         # transform
#         df_aux = df.copy()  # avoid changing original object
#         df_aux.columns = [col.replace("ID", "Id") for col in df_aux.columns]
#         df_aux.columns = [camelcase_to_snakecase(name=col) for col in df_aux.columns]
#
#         df_typed = df_aux.astype(conf["date_time_data_types_prm"])
#
#         df_renamed = df_typed.rename(columns={"order_date": "sales_date"})
#
#         df_dedup = df_renamed.drop_duplicates()
#
#         df_dedup.loc[:, "sales_year"] = df_dedup["sales_date"].dt.year
#
#         df_sorted = df_dedup.sort_values(by="sales_date", ascending=True)
#
#         df_sorted.loc[:, "time_id"] = np.arange(
#             start=1, stop=df_sorted.shape[0] + 1, step=1
#         )  # sum 1 because it starts in 0
#
#         # validate schema
#         date_time_prm_schema.validate(df_sorted)
#
#         # dump
#         dump_data_file(
#             df=df_sorted,
#             dump_base_path=conf["date_time_base_path_fte"],
#             file_name=dump_file_name,
#             file_type=dump_file_type,
#         )
#
#
# # date_time_primary()
