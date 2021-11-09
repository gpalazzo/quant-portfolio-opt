# from pathlib import Path
# import yaml
# from utils import read_data_file, dump_data_file
#
#
# root_path = Path(__file__).resolve().parents[4]
#
#
def dummy_intermediate() -> None:
    print("hello")
#     with open(f"{root_path}/conf/date_time.yml") as f:
#         conf = yaml.load(f, Loader=yaml.FullLoader)
#
#     for read_file_name, read_file_type, dump_file_name, dump_file_type in zip(
#         *[
#             conf["date_time_file_name_int"],
#             conf["date_time_file_type_int"],
#             conf["date_time_file_name_prm"],
#             conf["date_time_file_type_prm"],
#         ]
#     ):
#
#         # read
#         df = read_data_file(
#             read_base_path=conf["date_time_base_path_int"],
#             file_name=read_file_name,
#             file_type=read_file_type,
#         )
#
#         # transform
#         df_parsed = df[conf["date_time_cols_to_keep_int"]]
#
#         # dump
#         dump_data_file(
#             df=df_parsed,
#             dump_base_path=conf["date_time_base_path_prm"],
#             file_name=dump_file_name,
#             file_type=dump_file_type,
#         )
#
#
# # date_time_intermediate()
