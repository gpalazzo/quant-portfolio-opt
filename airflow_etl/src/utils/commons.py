from typing import List, Dict, Any
import yaml


def load_and_merge_ymls(paths: List[str]) -> Dict[Any, Any]:
    """Load yml files and merge then into one single dictionary

    Args:
        paths: list of strings representing paths to be loaded and merged

    Returns:
        dictionary with objects in yml files
    """

    merged_confs = {}

    # load all paths
    for path in paths:
        with open(path) as f:
            conf_aux = yaml.load(f, Loader=yaml.FullLoader)

        # check if there's any duplicated keys
        if set(merged_confs.keys()).intersection(conf_aux.keys()):
            raise ValueError("Trying to merge yml files with duplicated keys.")

        # build final merged dict
        merged_confs.update(conf_aux)

    return merged_confs
