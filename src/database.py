import json
import os
import pandas as pd
import numpy as np
import utils


class Make:
    # TODO get json file to load into a dataframe of items properly
    def __init__(self):
        self.afPath = ""  # Clear Alecaframe data path
        self.apiPath = ""  # Clear Data directory path
        temp, self.dataPath, self.afPath = utils.readConfig()  # Get data paths from config
        self.apiPath = self.dataPath + "/ApiData.json"  # Get local api path from data directory
        with open(self.apiPath) as file:
            self.apiData = json.dumps(file)
            pass
        # self.apiData = self.apiData[1]
        # self.apiData = pd.read_json(self.apiPath)

