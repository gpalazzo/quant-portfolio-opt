import pandas as pd
from typing import List


def read_data_file(
    read_base_path: str,
    file_name: str,
    file_type: str,
    sep: str = ";",
    encoding: str = "ISO-8859-1",
) -> pd.DataFrame:

    if file_type == "csv":
        return pd.read_csv(
            f"{read_base_path}/{file_name}.{file_type}", sep=sep, encoding=encoding
        )

    elif file_type == "parquet":
        return pd.read_parquet(f"{read_base_path}/{file_name}.{file_type}")

    else:
        raise TypeError("File type not supported.")


def dump_data_file(
    df: pd.DataFrame,
    dump_base_path: str,
    file_name: str,
    file_type: str,
    preserve_index: bool = False,
    partition_cols: List[str] = None,
) -> None:

    if file_type == "csv":
        df.to_csv(f"{dump_base_path}/{file_name}.{file_type}", index=preserve_index)

    elif file_type == "parquet":
        df.to_parquet(
            f"{dump_base_path}/{file_name}.{file_type}",
            index=preserve_index,
            partition_cols=partition_cols,
        )

    else:
        raise TypeError("File type not supported.")
