import os
import pandas as pd
import numpy as np


class Database:
    def __init__(self, dataPath, afPath):
        self.apiPath, self.afPath = os.path.join(dataPath, "ApiData.json"), afPath  # Set file paths as instance methods
        self.apiData = pd.read_json(self.apiPath)  # Make dataframe
