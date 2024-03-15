import datetime
import datetime as dt
import pandas as pd
import json


def getAPIPath(endpoint):
    """
    Parses and returns an API URL from endpoint.

    :param endpoint: Endpoint modifier.
    :type endpoint: str
    :return: Parsed URL.
    :rtype: str
    """
    base_url = "https://api.warframe.market"  # warframe.market base API URL
    version = "v1"  # Necessary version indicator for endpoint URL
    return f"{base_url}/{version}/{endpoint}"  # Parse the string params into endpoint URL


def readConfig():
    """
    Reads the config file, and returns the settings as separate variables.

    :return:Timestamp, Data directory path, and Alecaframe directory path in a tuple.
    :rtype: tuple[datetime.datetime, str, str]
    """
    with open("config.txt", 'r') as file:
        data = file.readlines()  # Read config
    Timestamp, dataDirectory = data[:2]  # Gather required config settings into variables
    dataDirectory = dataDirectory.strip()  # Strips the newline off of the stored API path
    alecaDirectory = data[2] if len(data) > 2 else ""  # Store Alecaframe data path if present
    Timestamp = dt.datetime.strptime(Timestamp[:-1],
                                     "%Y-%m-%d %H:%M:%S.%f")  # Cast timestamp to datetime
    return Timestamp, dataDirectory, alecaDirectory  # Return settings


def getDFFromAPIJSON(JSON_text, iter_name):
    """
    Takes JSON encoded text and parses it into a dataframe object.

    :param JSON_text: JSON text to parse
    :type JSON_text:
    :param iter_name: JSON key to iterate through to make each record
    :type iter_name: str
    :return: Dataframe of json text
    """

    data = pd.DataFrame()  # Assign the data attribute with an empty dataframe
    rawData = json.loads(JSON_text)  # Make dict from json response
    for key in rawData["payload"][iter_name]:
        # Grabs the json entry and puts it into a Series object
        # Casts the Series object into a Dataframe and then concats to the api_data.
        data = pd.concat([data, pd.DataFrame([pd.Series(key)])])
    return data


def getMeanPlat(item_df: pd.DataFrame, get_sell):
    """
    Takes dataframes of item orders and gets the average buy or sell price from them

    :param item_df: Dataframe of item orders.
    :param get_sell: Search for sell price.
    :type get_sell: bool
    :return: Average plat price
    :rtype: long
    """
    if get_sell:
        order_avg = item_df.loc[item_df['order_type'] == "sell"]
    else:
        order_avg = item_df.loc[item_df['order_type'] == "buy"]
    return round(pd.DataFrame.aggregate(order_avg['platinum'], func='mean'), 0)


def getMinMax(orders_df_dict: dict, get_sell):
    """
    Takes item orders dataframe, finds mean plat of each, and finds the best sell/buy item and its value.

    :param orders_df_dict: Dictionary of items and their order dataframe as its value.
    :param get_sell: Get the max selling item in the list if true, otherwise get the min buying item in the list.
    :type get_sell: bool
    :return: best priced item name, best priced item price
    :rtype: tuple[str, int]
    """
    mean_plat_dict = {}
    for item_name in orders_df_dict:
        # Get mean plat prices from dataframes
        mean_plat_dict[item_name] = getMeanPlat(orders_df_dict[item_name], get_sell)

    if get_sell:
        # Get max sell item and value from mean prices
        best_item_price, best_item_name = max(zip(mean_plat_dict.values(), mean_plat_dict.keys()))
    else:
        # Get min buy item and value from mean prices
        best_item_price, best_item_name = min(zip(mean_plat_dict.values(), mean_plat_dict.keys()))

    if best_item_price - round(best_item_price) == 0:  # If whole number, truncate decimal places
        best_item_price = round(best_item_price)

    return best_item_name, best_item_price  # Return best item name and price
