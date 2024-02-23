import os
import pandas as pd
import numpy as np
import utils


class Database:
    def __init__(self):
        self.afPath, self.dataPath, temp = None  # Set instance attrbute to none
        temp, self.dataPath, self.afPath .readConfig()  # Get data paths from config
        self.apiPath= os.path.join(self.dataPath, "ApiData.json")  # Get local api path from data directory
        self.apiData = pd.read_json(self.apiPath)  # Make dataframe
