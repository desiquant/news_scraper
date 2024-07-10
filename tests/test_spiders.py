from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from ..news_scraper.spiders import (
    BusinessStandardSpider,
    BusinessTodaySpider,
    EconomicTimesSpider,
    FinancialExpressSpider,
    FirstPostSpider,
    FreePressJournalSpider,
    IndianExpressSpider,
    MoneyControlSpider,
    NDTVProfitSpider,
    News18Spider,
    OutlookIndiaSpider,
    TheHinduSpider,
    TheHinduBusinessLineSpider,
    ZeeNewsSpider,
)

settings = get_project_settings()

# update some settings to make them test friendly
settings.update(
    {
        "SKIP_URLS_IN_OUTPUT": False,  # Do not skip URLs that have already been processed
        "CLOSESPIDER_ITEMCOUNT": 5,  # Stop after scraping 5 items
        "CLOSESPIDER_PAGECOUNT": 5,  # Stop after crawling 10 pages
        "CLOSESPIDER_TIMEOUT": 60,  # Stop after 60 seconds,
        "FEED_URI": "test-output.jl",  # Save the outputs to a new temporary file
        "HTTPCACHE_ENABLED": False,  # Do not cache requests
    }
)


process = CrawlerProcess(settings=settings)


def test_spider():
    spider = BusinessStandardSpider
    process.crawl(spider)
    process.start()
