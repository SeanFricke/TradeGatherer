import os.path
import pytest
from ..Utils import api


if os.path.exists("config.txt"):
    os.remove("config.txt")
testMarket = api.Make()

def test_config_make():
    assert os.path.exists("config.txt")


def test_apiData_make():
    dataDir = testMarket.dataDir
    assert os.path.exists(os.path.join(dataDir, "ApiData.json"))
