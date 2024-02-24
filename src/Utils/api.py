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
    __apiTimestamp = None  # Timestamp of last update
    alecaDir = ""  # Directory that holds any Alecaframe export data
    dataDir = ""  # Directory in which

    def __init__(self):
        self.timeAtOpen = dt.datetime.now()  # Get current time at process open, and save as variable
        # If config does not exist, create from scratch
        if not path.exists(self.CONFIG_PATH):
            # Prompt for directory to store API data in
            self.dataDir = filedialog.askdirectory(mustexist=True, initialdir="..", title="Select a directory for "
                                                                                          "the local data")
            self.__updateConfig(self.timeAtOpen, self.dataDir, self.alecaDir)
            self.__apiSync(True)  # Make new config file, and use prefs for API syncing
        else:
            self.__apiSync()  # Sync data if needed
            self.__updateConfig(self.__apiTimestamp, self.dataDir, self.alecaDir)  # Save any new timestamp to config

    def __apiSync(self, manualSync=False):
        """
        Checks if the local data needs to be synced with the API, depending on the age of the data.

        :param manualSync: (:class:`bool`) Force the function to manually sync the API data to local
        """
        self.__apiTimestamp, self.dataDir, self.alecaDir = utils.readConfig()  # Fetch config settings
        # If later than UPDATE_THRESHOLD days,
        # then sync the local API file to the API itself and write down new timestamp
        if self.__apiTimestamp <= self.timeAtOpen - self.UPDATE_THRESHOLD or manualSync:
            self.__updateApiFile()

    def __updateApiFile(self):
        """
       Syncs the Warframe.Market local file with the API.
       """
        apiPath = utils.getAPIPath("items")  # Get path to items endpoint of API
        dataPath = path.join(self.dataDir, "ApiData.json")  # Parse the API JSON file path from data directory
        with open(dataPath, "w") as file:
            json.dump(requests.get(apiPath).json(), file)  # Get item data from API and store to JSON file

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
        ordersPath = utils.getAPIPath(f"/items/{url}/orders")  # Parse URL
        args = {"Platform": self.platform}  # Set request params
        headers = {"Include": "item"}  # Set request headers
        # Make GET request for item orders
        return requests.get(ordersPath, params=args, headers=headers).json
