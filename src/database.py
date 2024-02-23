import os
import pandas as pd
import numpy as np
import utils


class Make:
    def __init__(self):
        self.afPath = ""  # Clear Alecaframe data path
        self.dataPath = ""  # Clear Data directory path
        temp = ""  # Clear temp file
        temp, self.dataPath, self.afPath = utils.readConfig()  # Get data paths from config
        self.apiPath= os.path.join(self.dataPath, "ApiData.json")  # Get local api path from data directory
        self.apiData = pd.read_json(self.apiPath)  # Make dataframe
