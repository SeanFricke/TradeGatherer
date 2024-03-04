from pathlib import Path
import pandas as pd
from src.Utils import utils


class Make:
    def __init__(self):
        self.afPath = ""  # Clear Alecaframe data path
        self.apiPath = ""  # Clear Data directory path
        self.apiData = None
        self.orderData = None
        self.order_Avg = None
        temp, self.dataPath, self.afPath = utils.readConfig()  # Get data paths from config
        self.apiPath = self.dataPath + "/ApiData.json"  # Get local api path from data directory
        self.apiData = utils.getDFFromAPIJSON(Path(self.apiPath).read_text(), "items")  # Create dataframe from api file

    def getOrderDF(self, API_obj, item):
        rawData = API_obj.getItemOrders(item)
        self.orderData = utils.getDFFromAPIJSON(rawData, "orders")

    def getMeanPlat(self, API_obj, item, list_sell=True):
        """
        Takes order listings of an item and takes the average buy or sell price
        :param API_obj: :class:`api` API market object.
        :param item: :class:`string` Item to get the mean price of.
        :param list_sell: :class:`bool` search for sell price.
        :return:
        """
        self.getOrderDF(API_obj,item)
        if list_sell:
            self.order_Avg = self.orderData.loc[self.orderData['order_type'] == "sell"]
        else:
            order_Avg = self.orderData.loc[self.orderData['order_type'] == "buy"]
        self.order_Avg = round(pd.DataFrame.aggregate(self.orderData['platinum'], func='mean'), 0)

