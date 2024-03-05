import os.path
import pytest
from src.Utils import api

if os.path.exists("config.txt"):
    os.remove("config.txt")
testMarket = api.API()


def test_config_make():
    assert os.path.exists("config.txt")


def test_apiData_make():
    dataDir = testMarket.data_dir
    assert os.path.exists(os.path.join(dataDir, "ApiData.json"))
