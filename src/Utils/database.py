from pathlib import Path
import pandas as pd
from src.Utils import utils


class Database:
    def __init__(self, api_obj):
        self.af_path = self.api_path = ""
        self.api_obj = api_obj

        temp, self.data_path, self.af_path = utils.readConfig()  # Get data paths from config
        self.api_path = self.data_path + "/ApiData.json"  # Get local api path from data directory
        self.api_data = utils.getDFFromAPIJSON(Path(self.api_path).read_text(),
                                               "items")  # Create dataframe from api file

    def getOrderDF(self, item):
        raw_data = self.api_obj.getItemOrders(item)
        return utils.getDFFromAPIJSON(raw_data, "orders")

    def getMeanPlat(self, item, list_sell):
        """
        Takes order listings of an item and takes the average buy or sell price

        :param item: Item to get the mean price of.
        :type item: str
        :param list_sell: Search for sell price.
        :type list_sell: bool
        :return: Average plat price
        :rtype: long
        """
        data = self.getOrderDF(item)
        if list_sell:
            order_avg = data.loc[data['order_type'] == "sell"]
        else:
            order_avg = data.loc[data['order_type'] == "buy"]
        return round(pd.DataFrame.aggregate(order_avg['platinum'], func='mean'), 0)

    def searchItems(self, item_list):
        """
        Collects the orders of a list of item URLs and groups them into a dict of dataframes.

        :param item_list: Collection of item urls to search for.
        :type item_list: list
        :return: Dict of order dataframes with key matching the item URL
        :rtype: dict
        """
        order_collection = {}
        for item in item_list:
            order_collection[item] = self.getOrderDF(item)
        return order_collection

