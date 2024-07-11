# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import itertools
import os

import netifaces
import pandas as pd

# useful for handling different item types with a single interface
from scrapy.exceptions import IgnoreRequest


def get_floating_ips(interface="eth0"):
    try:
        # Get all addresses for the specified interface
        addresses = netifaces.ifaddresses(interface)

        # Check if IPv4 addresses exist
        if netifaces.AF_INET in addresses:
            # Extract all IPv4 addresses
            ipv4_addresses = addresses[netifaces.AF_INET]

            # Filter for floating IPs (assuming they are secondary IPs)
            floating_ips = [addr["addr"] for addr in ipv4_addresses]

            return floating_ips
        else:
            return []
    except ValueError:
        print(f"Interface {interface} not found.")
        return []


class NewsScraperDownloaderMiddleware:
    # TODO: do not use floating ips in localhost
    floating_ips = itertools.cycle(get_floating_ips("eth0"))
    processed_urls = []

    def process_request(self, request, spider):
        # ignore urls which are already processed
        if request.url in self.processed_urls:
            raise IgnoreRequest

        # use all ips available on server
        if spider.settings.get("USE_FLOATING_IPS"):
            request.meta["bindaddress"] = (next(self.floating_ips), 0)

        # sample web proxy usage
        # request.meta["proxy"] = "http://user:pass@brd.superproxy.io:22225"

        return None

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

        if spider.settings.get("SKIP_URLS_IN_OUTPUT"):
            # TODO: make this dynamic output path
            output_file = (
                f"/home/skd/tmp/async-test/news_scraper/{spider.name}-output.jl"
            )

            if os.path.isfile(output_file):
                df = pd.read_json(output_file, lines=True)

                if not df.empty:
                    self.processed_urls = list(df["url"].unique())
                    spider.logger.info(
                        "Spider already processed: %s URLs" % len(self.processed_urls)
                    )
