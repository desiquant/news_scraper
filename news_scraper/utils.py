import os

import netifaces
import pandas as pd
from fake_useragent import UserAgent
from scrapy import Spider

ua = UserAgent()

yesterday = (pd.Timestamp.now() - pd.Timedelta(days=1)).normalize()


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


def get_output_urls(output_file: str) -> list[str]:
    """
    Retrieve a list of urls that are already saved in output file for a spider.
    """

    if os.path.isfile(output_file):
        df = pd.read_json(output_file, lines=True)
        if not df.empty:
            return list(df["url"].unique())

    return []
