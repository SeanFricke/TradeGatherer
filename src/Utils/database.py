import os.path
import time
from pathlib import Path
import pandas as pd
from src.Utils import utils, api
import multiprocessing as mp
import tqdm


class Database:
    def __init__(self, api_obj: api):
        self.af_path = self.api_path = ""
        self.api_obj = api_obj

        temp, self.data_path, self.af_path = utils.readConfig()  # Get data paths from config
        self.api_path = self.data_path + "/ApiData.json"  # Get local api path from data directory
        self.api_data = utils.getDFFromAPIJSON(Path(self.api_path).read_text(),
                                               "items")  # Create dataframe from api file

    def getOrderDF(self, item: str, raw_data=None, from_raw=False):
        if not from_raw:
            raw_data = self.api_obj.getItemOrders(item)
        return item, utils.getDFFromAPIJSON(raw_data, "orders")

    def searchItems(self, item_list, cache=False):
        """
        Collects the orders of a list of item URLs and groups them into a dict of dataframes.

        :param item_list: Collection of item urls to search for.
        :type item_list: list
        :param cache: Option to save and use a local copy of the orders of each item if enabled.
        Will only be needed for debugging only, as it does not resync after copy creation. (Defaults to False)
        :type cache: bool
        :return: Dict of order dataframes with key matching the item URL
        :rtype: dict
        """
        order_collection = {}
        for item in item_list:
            if cache:
                item_cache_path = self.data_path + f"/{item}.json"
                if os.path.exists(item_cache_path):
                    with open(item_cache_path, "r") as f:
                        raw_data = f.read()
                    _temp, order_collection[item] = self.getOrderDF(item, raw_data, from_raw=True)
                else:
                    raw_data = self.api_obj.getItemOrders(item)
                    with open(item_cache_path, "w") as f:
                        f.write(raw_data)
                    _temp, order_collection[item] = self.getOrderDF(item, raw_data, from_raw=True)
            else:
                _temp, order_collection[item] = self.getOrderDF(item)
        return order_collection

    def searchItemsAsync(self, url_list):
        """
        Asynchronous version of `searchItems` method.
        :param url_list: List of item URL's to search for
        :type url_list: list[str]
        :return:
        :rtype: dict[pandas.DataFrame]
        """
        results_list = {}
        api_num = 1
        with mp.Pool(round(len(url_list) * 0.75)) as p:
            for i, j in tqdm.tqdm(p.imap_unordered(self.getOrderDF, url_list), total=len(url_list)):
                results_list[i] = j
                if api_num % 3 == 0:
                    time.sleep(1)
                api_num += 1
        return results_list
