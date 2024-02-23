import datetime
import datetime as dt


def getAPIPath(endpoint):
    """
    Parses and returns an API URL from endpoint.

    :param endpoint:
        :class:`string` Endpoint modifier.
    :return:
        :class:`string` Parsed URL.
    """
    base_url = "https://api.warframe.market"  # warframe.market base API URL
    version = "v1"  # Necessary version indicator for endpoint URL
    return f"{base_url}/{version}/{endpoint}"  # Parse the string params into endpoint URL


def readConfig():
    """
    Reads the config file, and returns the settings as separate variables

    :return:
        | (:class:`datetime.datetime`) Timestamp
        | (:class:`string`) Data directory path
        | (:class:`string`) Alecaframe directory path
    """
    with open("config.txt", 'r') as file:
        data = file.readlines()  # Read config
    Timestamp, dataDirectory = data[:2]  # Gather required config settings into variables
    dataDirectory = dataDirectory.strip()  # Strips the newline off of the stored API path
    alecaDirectory = data[2] if len(data) > 2 else ""  # Store Alecaframe data path if present
    Timestamp = dt.datetime.strptime(Timestamp[:-1],
                                     "%Y-%m-%d %H:%M:%S.%f")  # Cast timestamp to datetime
    return Timestamp, dataDirectory, alecaDirectory  # Return settings
