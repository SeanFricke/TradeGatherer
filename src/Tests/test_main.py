import pandas as pd
import pytest
from src.Utils import api, database


class TestMain:
    test_Market = None
    test_database = None

    @pytest.fixture
    def test_construct_database(self):
        self.test_Market = api.Make()
        self.test_database = database.Make()

    def test_database_class(self, test_construct_database):
        assert type(self.test_database.apiData) == pd.DataFrame

    def test_database_orders(self, test_construct_database):
        item = "secura_dual_cestra"
        self.test_database.getOrderDF(self.test_Market, item)
        assert type(self.test_database.apiData) == pd.DataFrame

    def test_order_mean_sell(self, test_construct_database):
        item = "secura_dual_cestra"
        self.test_database.getMeanPlat(self.test_Market, item)
        assert 1 < self.test_database.order_Avg < 300

    def test_order_mean_buy(self, test_construct_database):
        item = "secura_dual_cestra"
        self.test_database.getMeanPlat(self.test_Market, item, list_sell=False)
        assert 1 < self.test_database.order_Avg < 300
