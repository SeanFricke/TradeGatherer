def getAPIPath(endpoint):
    """
    Parses and returns an API URL from endpoint.

    :param endpoint: :class:`String <str>` Endpoint modifier.
    :return: :class:`String <str>` Parsed URL.
    """
    base_url = "https://api.warframe.market"  # warframe.market base API URL
    version = "v1"  # Necessary version indicator for endpoint URL
    return f"{base_url}/{version}/{endpoint}"  # Parse the string params into endpoint URL
