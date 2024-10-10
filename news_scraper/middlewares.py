# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import itertools
import os
from scrapy import Spider, crawler, signals
from scrapy.exceptions import IgnoreRequest
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
from .utils import get_interface_ips, get_spider_output

#Mask the sensitive parts of the proxy URL (user:password).
def mask_proxy_url(proxy_url):
    if '@' in proxy_url:
        proxy_parts = proxy_url.split('@')
        if ':' in proxy_parts[0]:
            masked_user = proxy_parts[0].split(':')[0] + ":****"
            return masked_user + "@" + proxy_parts[1]
    return proxy_url

class NewsScraperDownloaderMiddleware:
    floating_ips = get_interface_ips()
    output_urls = []

    @property
    def floating_ips_cycle(self):
        return itertools.cycle(self.floating_ips)

    @classmethod
    def from_crawler(cls, crawler: crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def spider_opened(self, spider: Spider):
        spider.logger.info("Spider opened: %s" % spider.name)

        # show ips currently in use
        spider.logger.info(
            "Floating IPs (total: %s): %s" % (len(self.floating_ips), self.floating_ips)
        )

        # load already parsed urls
        if spider.settings.getbool("SKIP_OUTPUT_URLS"):
            for output_file, _ in spider.settings.getdict("FEEDS").items():
                df = get_spider_output(output_file)
                self.output_urls = list(df["url"].unique()) if not df.empty else []

                spider.logger.info(
                    "Already scraped %s URLs in: %s"
                    % (len(self.output_urls), output_file)
                )

    def process_request(self, request, spider: Spider):
        # ignore urls which are already processed
        if request.url in self.output_urls:
            spider.logger.info("Ignoring Request (already in output): %s", request.url)
            raise IgnoreRequest

        # if spider.settings.getbool("USE_PROXY"):
        #   request.meta["proxy"] = "http://user:pass@brd.superproxy.io:22225"
        if spider.settings.getbool("USE_PROXY"):
            proxy_url = os.getenv("PROXY_URL")
            masked_proxy_url=mask_proxy_url(proxy_url)
            request.meta["proxy"] = proxy_url
            spider.logger.info(f"Using proxy:{masked_proxy_url}")

        # use all ips available on server
        if spider.settings.getbool("USE_FLOATING_IPS"):
            if self.floating_ips:
                request.meta["bindaddress"] = (next(self.floating_ips_cycle), 0)

        return None
