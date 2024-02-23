import os.path
import pytest
import api


@pytest.fixture
def test_api_first_boot():
    if os.path.exists("config.txt"):
        os.remove("config.txt")


def test_config_make(test_api_first_boot):
    test_api_first_boot
    testMarket = api.MarketAPI()
    del testMarket
    assert os.path.exists("config.txt")

def test_apiData_make(test_api_first_boot):
    test_api_first_boot
    testMarket = api.MarketAPI()
    assert os.path.exists(os.path.join(testMarket.dataDir, "ApiData.json"))
    del testMarket