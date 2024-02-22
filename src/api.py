import json
import requests
from os import pat
import datetime as dt


class MarketAPI:
    UPDATE_THRESHOLD = dt.timedelta(days=10)  # Threshold in which to sync the local files
    CONFIG_PATH = path.join("Data", "config.txt")
    apiData = ""
    apiTimestamp = None
    afData = ""

    def __init__(self):
        """
        Starts the class by checking for updates with the local files.
        """
        timeAtOpen = dt.datetime.now()  # Get current time at process open, and save as variable
        with open(self.CONFIG_PATH, 'r') as file:
            data = file.readlines()  # Read config
        self.apiData, self.apiTimestamp = data[:2]  # Gather required config lines into variables
        self.apiData = self.apiData.strip()  # Strips the newline off of the stored API path
        self.afData = data[2] if len(data) > 2 else ""  # Store Alecaframe data path if present
        self.apiTimestamp = dt.datetime.strptime(self.apiTimestamp[:-1], "%Y-%m-%d %X")  # Cast timestamp to datetime
        # If later than UPDATE_THRESHOLD days, then sync the local API file to the API itself and write down new timestamp
        if self.apiTimestamp <= timeAtOpen - self.UPDATE_THRESHOLD:
            self.__updateApiFile()
            self.__updateConfig(self.apiData, timeAtOpen, self.afData)

    def __updateApiFile(self):
        """
       Syncs the Warframe.Market local file with the API.
       """
        apiPath = self.__getAPIPath("items")
        with open(self.apiData, 'w') as file:
            file.write(json.dumps(requests.get(apiPath).json()))

    def __updateConfig(self, *data):
        """
        Updates the config file with the given lines of data.

        :param data: Config data, per line.
        """
        with open(self.CONFIG_PATH, 'w') as file:
            for i in data:
                file.write(str(i) + "\n")

    def __getAPIPath(self, endpoint):
        """
        Parses and returns an API URL from endpoint.

        :param endpoint: :class:`String <str>` Endpoint modifier.
        :return: :class:`String <str>` Parsed URL.
        """
        base_url = "https://api.warframe.market"  # warframe.market base API URL
        version = "v1"  # Necessary version indicator for endpoint URL
        return f"{base_url}/{version}/{endpoint}"  # Parse the string params into endpoint URL

    def getItemOrders(self, url, platform="pc"):
        """
        Returns a JSON response from the market with a list of orders of an item name.

        :param platform: :class:`String <str>` (Optional) Platform on which to filter the orders by.
        :param url: :class:`String <str>` URL of item on warframe.market.
        :return: :class:`Dictionary <builtins.dict>` JSON response.
        """
        path = self.__getAPIPath(f"/items/{url}/orders")  # Parse URL
        args = {"Platform": platform}  # Set request params
        headers = {"Include": "item"}  # Set request headers
        return requests.get(path, params=args, headers=headers).json()  # Make GET request for item orders
