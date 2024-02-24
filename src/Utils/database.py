from pathlib import Path
import pandas as pd
from src.Utils import utils


class Make:
    def __init__(self):
        self.afPath = ""  # Clear Alecaframe data path
        self.apiPath = ""  # Clear Data directory path
        self.apiData = None
        self.orderData = None
        temp, self.dataPath, self.afPath = utils.readConfig()  # Get data paths from config
        self.apiPath = self.dataPath + "/ApiData.json"  # Get local api path from data directory
        self.apiData = utils.getDFFromAPIJSON(Path(self.apiPath).read_text())  # Create dataframe from api file
