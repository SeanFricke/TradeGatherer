import os.path
import pytest
import api


@pytest.fixture
def test_clean_config():
    if os.path.exists("config.txt"):
        os.remove("config.txt")


def test_config_make(test_clean_config):
    test_clean_config
    testMarket = api.Make()
    del testMarket
    assert os.path.exists("config.txt")


def test_apiData_make(test_clean_config):
    test_clean_config
    testMarket = api.Make()
    dataDir = testMarket.dataDir
    del testMarket
    assert os.path.exists(os.path.join(dataDir, "ApiData.json"))
