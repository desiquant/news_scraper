import os

import netifaces
import pandas as pd
from fake_useragent import UserAgent

ua = UserAgent()


def get_interface_ips(interface="eth0"):
    """
    Returns a list of all IPs available on an interface. To use be used to retrieve all floating IPs attached to a server and cycle through these IPs while making requests.
    """
    try:
        ifaddresses = netifaces.ifaddresses(interface)
        floating_ips = [i["addr"] for i in ifaddresses[netifaces.AF_INET]]
        return floating_ips
    except Exception:
        return []


def get_spider_output(output_file: str) -> pd.DataFrame:
    """Returns the saved spider output as a pandas DataFrame"""

    if os.path.isfile(output_file):
        df = pd.read_json(output_file, lines=True)

        # parse some required date columns
        for c in ["date_published", "date_modified"]:
            df[c] = pd.to_datetime(df[c], format="mixed").dt.tz_localize(None)

    else:
        df = pd.DataFrame()

    return df
