import datetime as dt
import json
from os import path
import requests
from tkinter import filedialog
from src.Utils import utils


class Make:
    UPDATE_THRESHOLD = dt.timedelta(days=10)  # Threshold in which to sync the local files
    CONFIG_PATH = "config.txt"  # Path to config file
    platform = "pc"  # Platform on which to get API data from
    __api_timestamp = None  # Timestamp of last update
    aleca_dir = ""  # Directory that holds any Alecaframe export data
    data_dir = ""  # Directory in which

    def __init__(self):
        self.time_at_open = dt.datetime.now()  # Get current time at process open, and save as variable
        # If config does not exist, create from scratch
        if not path.exists(self.CONFIG_PATH):
            # Prompt for directory to store API data in
            self.data_dir = filedialog.askdirectory(mustexist=True, initialdir="..", title="Select a directory for "
                                                                                          "the local data")
            self.__updateConfig(self.time_at_open, self.data_dir, self.aleca_dir)
            self.__apiSync(True)  # Make new config file, and use prefs for API syncing
        else:
            self.__apiSync()  # Sync data if needed
            self.__updateConfig(self.__api_timestamp, self.data_dir, self.aleca_dir)  # Save any new timestamp to config

    def __apiSync(self, manual_sync=False):
        """
        Checks if the local data needs to be synced with the API, depending on the age of the data.

        :param manual_sync: (:class:`bool`) Force the function to manually sync the API data to local
        """
        self.__api_timestamp, self.data_dir, self.aleca_dir = utils.readConfig()  # Fetch config settings
        # If later than UPDATE_THRESHOLD days,
        # then sync the local API file to the API itself and write down new timestamp
        if self.__api_timestamp <= self.time_at_open - self.UPDATE_THRESHOLD or manual_sync:
            self.__updateApiFile()

    def __updateApiFile(self):
        """
       Syncs the Warframe.Market local file with the API.
       """
        api_path = utils.getAPIPath("items")  # Get path to items endpoint of API
        data_path = path.join(self.data_dir, "ApiData.json")  # Parse the API JSON file path from data directory
        with open(data_path, "w") as file:
            json.dump(requests.get(api_path).json(), file)  # Get item data from API and store to JSON file

    def __updateConfig(self, *data):
        """
        Updates the config file with the given lines of data.

        :param data: :class:`String <str>` Config data, per line.
        """
        with open(self.CONFIG_PATH, 'w') as file:
            for i in data:
                file.write(str(i) + "\n")  # Write all data args to file, seperated by a newline

    def getItemOrders(self, url):
        """
        Returns a JSON response from the market with a list of orders of an item name.

        :param url: :class:`String <str>` URL of item on warframe.market.
        :return: :class:`Dictionary <builtins.dict>` JSON response.
        """
        orders_path = utils.getAPIPath(f"/items/{url}/orders")  # Parse URL
        args = {"Platform": self.platform}  # Set request params
        headers = {"Include": "item"}  # Set request headers
        # Make GET request for item orders
        return requests.get(orders_path, params=args, headers=headers).text
