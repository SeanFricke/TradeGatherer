from pathlib import Path
import pandas as pd
from src.Utils import utils


class Make:
    def __init__(self):
        self.af_Path = ""  # Clear Alecaframe data path
        self.api_Path = ""  # Clear Data directory path
        self.api_Data = None
        self.order_Data = None
        self.order_Avg = None

        temp, self.data_path, self.af_Path = utils.readConfig()  # Get data paths from config
        self.api_Path = self.data_path + "/ApiData.json"  # Get local api path from data directory
        self.api_Data = utils.getDFFromAPIJSON(Path(self.api_Path).read_text(),
                                               "items")  # Create dataframe from api file

    def getOrderDF(self, API_obj, item):
        raw_data = API_obj.getItemOrders(item)
        self.order_Data = utils.getDFFromAPIJSON(raw_data, "orders")

    def getMeanPlat(self, API_obj, item, list_sell):
        """
        Takes order listings of an item and takes the average buy or sell price
        :param API_obj: :class:`api` API market object.
        :param item: :class:`string` Item to get the mean price of.
        :param list_sell: :class:`bool` search for sell price.
        :return:
        """
        self.getOrderDF(API_obj, item)
        if list_sell:
            self.order_Avg = self.order_Data.loc[self.order_Data['order_type'] == "sell"]
        else:
            order_Avg = self.order_Data.loc[self.order_Data['order_type'] == "buy"]
        self.order_Avg = round(pd.DataFrame.aggregate(self.order_Data['platinum'], func='mean'), 0)
