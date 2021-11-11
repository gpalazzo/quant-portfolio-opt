from typing import List, Dict, Any
import re
import pandas as pd
import yaml


def std_raw_df_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Apply rules to standardize raw dataframe columns

    Args:
        df: pandas dataframe to apply rules

    Returns:
        pandas dataframe with data standardized by the pre-defined rules
    """

    for col in df.columns:
        df.loc[:, col] = df.loc[:, col].astype(str)

    return df


def load_and_merge_ymls(paths: List[str]) -> Dict[Any, Any]:
    """Load yml files and merge then into one single dictionary

    Args:
        paths: list of strings representing paths to be loaded

    Returns:
        dictionary with objects in yml files
    """

    merged_confs = {}

    for path in paths:
        with open(path) as f:
            conf_aux = yaml.load(f, Loader=yaml.FullLoader)

        if set(merged_confs.keys()).intersection(conf_aux.keys()):
            raise ValueError("Trying to merge yml files with duplicated keys.")

        merged_confs.update(conf_aux)

    return merged_confs


def camelcase_to_snakecase(name: str) -> str:
    return name[0].lower() + re.sub(
        r"(?!^)[A-Z]", lambda x: "_" + x.group(0).lower(), name[1:]
    )
