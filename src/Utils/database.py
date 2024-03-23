import os.path
import time
from pathlib import Path
import pandas as pd
from src.Utils import utils, api
import multiprocessing as mp
import tqdm
import rapidfuzz as rf


class Database:
    def __init__(self, api_obj: api):
        self.af_path = self.api_path = ""
        self.api_obj = api_obj
        self.items_df = {}

        temp, self.data_path, self.af_path = utils.readConfig()  # Get data paths from config
        self.api_path = self.data_path + "/ApiData.json"  # Get local api path from data directory
        self.api_data = utils.getDFFromJSON(Path(self.api_path).read_text(),
                                            "items")  # Create dataframe from api file

        self.__getItemURLDict()  # Create Item name/URL dict

    def __getItemURLDict(self):
        """
        Creates a dictionary of each item's name and corresponding URL, saving it into the 'items_df' attribute.
        """

        # Open ApiData.json and read its data.
        with open(self.api_path, "r") as f:
            rawData = f.read()

        api_df = utils.getDFFromJSON(rawData, "items")  # Make dataframe from JSON data

        # Process and clean dataframe
        # Turn dataframe into dictionary of key-value pair of item name, with value of the item url.
        api_df = api_df[["item_name", "url_name"]].set_index("item_name").to_dict()
        self.items_df = api_df["url_name"]  # Save dictionary to attribute

    def getOrderDF(self, item_url: str):
        """
        Takes item url and gets the dataframe of the orders list of that item.
        :param item_url: url of item to get the orders from
        :return: url of item and its corresponding dataframe of orders
        :rtype: tuple[str, pandas.DataFrame]
        """
        raw_data = self.api_obj.getItemOrders(item_url)  # Get order JSON of item from API
        return item_url, utils.getDFFromJSON(raw_data, "orders")  # Turn order JSON into dataframe

    def searchOrders(self, item_list, cache=False):
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
                    order_collection[item] = utils.getDFFromJSON(raw_data, "orders")
                else:
                    raw_data = self.api_obj.getItemOrders(item)
                    with open(item_cache_path, "w") as f:
                        f.write(raw_data)
                    order_collection[item] = utils.getDFFromJSON(raw_data, "orders")
            else:
                _temp, order_collection[item] = self.getOrderDF(item)
        return order_collection

    def searchOrdersAsync(self, url_list):
        """
        Asynchronous version of `searchItems` method.
        :param url_list: List of item URLs to search for
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

    def searchItems(self, search_string: str, scorer=rf.fuzz.partial_token_ratio, limit=100):
        """
        Find related items to a search string, and return a dataframe of the resulting items and corresponding URL

        :param search_string: Search query
        :param limit: Max number of results to find
        :type limit: int
        :param scorer: rapidfuzz.fuzz scorer to use with searching.
        :return: Dataframe of top 100 related item names and their urls
        :rtype: pandas.DataFrame
        """
        search_results_df = pd.DataFrame(columns=["Name", "URL"], index=["Name"])
        search_results = rf.process.extract(search_string, self.items_df.keys(), scorer=scorer,
                                            limit=limit, score_cutoff=100, processor=rf.utils.default_process)
        for result in search_results:
            result_series = pd.Series(data={"Name": result[0], "URL": self.items_df[result[0]]})
            search_results_df = pd.concat([search_results_df, result_series.to_frame().T])

        search_results_df.dropna(inplace=True)
        search_results_df.set_index("Name", inplace=True)

        return search_results_df
