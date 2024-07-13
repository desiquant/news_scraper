import json
import multiprocessing
import os
import subprocess

import pandas as pd
import pytest
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import Settings, get_project_settings

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
    ]
)
def spider(request):
    return request.param


def run_spider(spider: Spider, settings: Settings):
    process = CrawlerProcess(settings)
    process.crawl(spider)
    process.start()


def test_spider_crawl(spider: Spider):
    output_file = f"outputs-process-test/{spider.name}.jl"

    # remove output if exists
    if os.path.isfile(output_file):
        os.remove(output_file)

    settings = get_project_settings()
    settings.update(
        {
            "SKIP_OUTPUT_URLS": False,  # Do not skip URLs that have already been processed
            "CLOSESPIDER_ITEMCOUNT": 10,  # Stop after scraping 5 items
            "CONCURRENT_REQUESTS": 5,  # If default concurrent is used, it ignores itemcount limit
            "CLOSESPIDER_TIMEOUT": 30,  # Stop after 30 seconds,
            # Save the outputs to a new temporary file
            "FEEDS": {output_file: {"format": "jsonlines", "overwrite": True}},
            "HTTPCACHE_ENABLED": False,  # Do not cache requests, # ! TEMP: disable cache
            "LOG_FILE": "test-run.log",  # Prevent log from writing to stdout,
        }
    )

    p = multiprocessing.Process(
        target=run_spider,
        args=(
            spider,
            settings,
        ),
    )
    p.start()
    p.join()

    # check if spider created output
    if not os.path.isfile(output_file):
        raise FileNotFoundError(output_file)

    df = pd.read_json(output_file, lines=True)

    output_cols = set(df.columns)
    required_cols = {
        "url",
        "title",
        "description",
        "author",
        "date_published",
        "date_modified",
        "article_text",
        "scrapy_scraped_at",
        "scrapy_parsed_at",
    }

    assert output_cols == required_cols
