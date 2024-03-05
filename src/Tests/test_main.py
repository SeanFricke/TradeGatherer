import pandas as pd
import pytest
from src.Utils import api, database


class TestMain:
    test_Market = None
    test_database = None

    @pytest.fixture
    def test_construct_database(self):
        self.test_Market = api.API()
        self.test_database = database.Database(self.test_Market)

    def test_database_class(self, test_construct_database):
        assert type(self.test_database.api_data) == pd.DataFrame

    def test_database_orders(self, test_construct_database):
        item = "secura_dual_cestra"
        self.test_database.getOrderDF(item)
        assert type(self.test_database.api_data) == pd.DataFrame

    def test_order_mean_sell(self, test_construct_database):
        item = "secura_dual_cestra"
        self.test_database.getMeanPlat(item, True)
        assert 1 < self.test_database.order_avg < 300

    def test_order_mean_buy(self, test_construct_database):
        item = "secura_dual_cestra"
        self.test_database.getMeanPlat(item, False)
        assert 1 < self.test_database.order_avg < 300
