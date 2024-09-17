import os
from datetime import datetime

from .utils import get_interface_ips

###################
# Custom Settings #
###################

# scrapes articles only within the given date range
DATE_RANGE = (datetime.today(), datetime.now())  # scrapes only articles published today
# DATE_RANGE = ("2020-01-01", datetime.now()) # scrape all articles from 2020 until today

SKIP_OUTPUT_URLS = True  # skips fetching, parsing already existing urls in output
USE_FLOATING_IPS = True  # uses additional floating ips if available on network


####################
# Default Settings #
####################

# Scrapy provides in-built settings, most of which are auto-populated in new projects.
# We've modified a few settings for our use case.
# Default settings can be found here: https://github.com/scrapy/scrapy/blob/master/scrapy/settings/default_settings.py


# Basic Settings
BOT_NAME = "news_scraper"
SPIDER_MODULES = ["news_scraper.spiders"]
NEWSPIDER_MODULE = "news_scraper.spiders"

# User Agent Settings
USER_AGENT = "Googlebot-News/2.1 (+http://www.google.com/bot.html)"
# USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

# Robot Settings
ROBOTSTXT_OBEY = False

# Request Retry Settings
RETRY_HTTP_CODES = [
    500,
    502,
    503,
    504,
    522,
    524,
    408,
    403,  # if blocked by domain
    429,
]

# Concurrency Settings
total_processors = os.cpu_count()
total_floating_ips = len(get_interface_ips())
CONCURRENT_REQUESTS = 16 * min(4 * total_processors, 20)
CONCURRENT_REQUESTS_PER_DOMAIN = 8 * (total_floating_ips + 1)
CONCURRENT_ITEMS = 100 * total_processors

# Cookie Settings
COOKIES_ENABLED = False

# Downloader Middlewares
DOWNLOADER_MIDDLEWARES = {
    "news_scraper.middlewares.NewsScraperDownloaderMiddleware": 543
}

# HTTP Cache Settings
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = "httpcache"
HTTPCACHE_IGNORE_HTTP_CODES = [403]
HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Feed Settings
FEED_EXPORT_ENCODING = "utf-8"
FEED_EXPORTERS = {
    "jsonlines": "news_scraper.exporters.OrderedJsonLinesItemExporter",
}


# Future-proof Settings
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
