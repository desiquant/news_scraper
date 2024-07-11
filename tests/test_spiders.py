import pandas as pd
import pytest
from scrapy.crawler import CrawlerProcess, Spider
from scrapy.utils.project import get_project_settings

from news_scraper.spiders import (
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
    TheHinduBusinessLineSpider,
    TheHinduSpider,
    ZeeNewsSpider,
)


@pytest.fixture(
    params=[
        # BusinessStandardSpider,
        # BusinessTodaySpider,
        # EconomicTimesSpider,
        # FinancialExpressSpider,
        # FirstPostSpider,
        # FreePressJournalSpider,
        # IndianExpressSpider,
        # MoneyControlSpider,
        # NDTVProfitSpider,
        # News18Spider,
        # OutlookIndiaSpider,
        # TheHinduSpider,
        # TheHinduBusinessLineSpider,
        ZeeNewsSpider
    ]
)
def spider(request):
    return request.param


def test_spider(spider: Spider):
    settings = get_project_settings()
    output_file = f"outputs-test/{spider.name}.jl"

    # update some settings to make them test friendly
    settings.update(
        {
            "SKIP_URLS_IN_OUTPUT": False,  # Do not skip URLs that have already been processed
            "CLOSESPIDER_ITEMCOUNT": 5,  # Stop after scraping 5 items
            "CLOSESPIDER_TIMEOUT": 60,  # Stop after 60 seconds,
            # Save the outputs to a new temporary file
            "FEEDS": {output_file: {"format": "jsonlines", "overwrite": True}},
            "HTTPCACHE_ENABLED": True,  # Do not cache requests, # ! TEMP: disable cache
            "LOG_FILE": "/tmp/scrapy-test-run.log",  # Prevent log from writing to stdout
        }
    )

    # run the spider
    process = CrawlerProcess(settings=settings)
    process.crawl(spider)
    process.start()

    # check the output of the spider
    df = pd.read_json(output_file, lines=True)

    output_cols = set(df.columns)
    required_cols = {
        "url",
        "title",
        "description",
        "author",
        "date_published",
        "date_modified",
        "article_html",
        "scrapy_scraped_at",
        "scrapy_parsed_at",
    }

    assert output_cols == required_cols
