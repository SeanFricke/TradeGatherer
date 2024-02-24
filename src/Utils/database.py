import json
import os
from pathlib import Path

import pandas as pd
import numpy as np
from src.Utils import utils


class Make:
    # TODO get json file to load into a dataframe of items properly
    def __init__(self):
        self.afPath = ""  # Clear Alecaframe data path
        self.apiPath = ""  # Clear Data directory path
        temp, self.dataPath, self.afPath = utils.readConfig()  # Get data paths from config
        self.apiPath = self.dataPath + "/ApiData.json"  # Get local api path from data directory
        raw_json_dict = json.loads(Path(self.apiPath).read_text())
        self.apiData = pd.DataFrame()
        for key in raw_json_dict["payload"]["items"]:
            # Grabs the json entry and puts it into a Series object
            # Casts the Series object into a Dataframe and then concats to the apiData.
            self.apiData = pd.concat([self.apiData, pd.DataFrame([pd.Series(key)])])
