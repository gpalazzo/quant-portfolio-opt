import pytest
from pathlib import Path
from kedro.config import ConfigLoader


@pytest.fixture
def parameters():
    conf_paths = str(Path(__file__).resolve().parents[2] / "conf/base/")
    conf = ConfigLoader(conf_paths=conf_paths)
    params = conf.get("parameters*/**")
    return params
