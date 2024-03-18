import time

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

    def test_database_orders(self, test_construct_database):
        item = "secura_dual_cestra"
        _temp, data = self.test_database.getOrderDF(item)
        assert type(data) == pd.DataFrame

    def test_order_mean_sell(self, test_construct_database):
        item = "secura_dual_cestra"
        assert 1 < self.test_database.getMeanPlat(item, True) < 300

    def test_order_mean_buy(self, test_construct_database):
        item = "secura_dual_cestra"
        assert 1 < self.test_database.getMeanPlat(item, False) < 300

    def test_item_search(self, test_construct_database):
        start_time = time.time()
        items = ["strun_wraith_receiver", "mantis_set", "fluctus_limbs", "secura_dual_cestra"]
        data = self.test_database.searchItems(items)
        end_time = time.time()
        print(end_time - start_time)
        assert type(data) == dict and len(data) == len(items)

    def test_item_async_search(self, test_construct_database, threads):
        start_time = time.time()
        items = ["strun_wraith_receiver", "mantis_set", "fluctus_limbs", "secura_dual_cestra"]
        data = self.test_database.searchItemsAsync(items)
        end_time = time.time()
        print(end_time - start_time)
        assert type(data) == dict and len(data) == len(items)



