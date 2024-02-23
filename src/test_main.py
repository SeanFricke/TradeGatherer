import pandas as pd

import api, database, pytest


class TestMain:
    test_Market = None
    test_database = None

    @pytest.fixture
    def test_construct_Api(self):
        self.test_Market = api.Make()

    def test_database_class(self, test_construct_Api):
        test_construct_Api
        test_database = database.Make()
        assert type(test_database.apiData) == pd.DataFrame
