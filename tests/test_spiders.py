import json
import multiprocessing
import os
import re
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
    CnbcTv18Spider,
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
        CnbcTv18Spider,
    ]
)
def spider(request):
    return request.param


def run_spider(spider: Spider, settings: Settings):
    process = CrawlerProcess(settings)
    process.crawl(spider)
    process.start()


def test_spider_crawl(spider: Spider):
    output_file = f"outputs-crawl-test/{spider.name}.jl"

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
        },
        priority="cmdline",
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


@pytest.mark.parametrize(
    "url",
    [
        "https://www.business-standard.com/markets/news/railtel-stock-soars-18-on-heavy-volumes-up-331-in-1-year-124071200447_1.html",
        "https://www.businesstoday.in/markets/company-stock/story/hdfc-bank-shares-down-8-from-one-year-high-should-you-enter-at-current-levels-436040-2024-07-05",
        "https://economictimes.indiatimes.com/markets/stocks/news/it-stocks-in-focus-ahead-of-june-qtr-results-tcs-cyient-top-buy-which-could-give-15-18-return/articleshow/111569297.cms",
        "https://www.financialexpress.com/market/will-markets-crash-ahead-of-budget-is-it-the-right-time-to-book-profitsnbsp-check-key-nifty-levels-to-watch-3549556/",
        "https://www.firstpost.com/business/rs-147-5-debited-from-your-sbi-account-heres-why-state-bank-of-india-has-done-this-11792501.html",
        "https://www.freepressjournal.in/business/sbi-raises-10000-cr-via-sixth-infrastructure-bond-issuance-at-736-coupon-rate-oversubscribed-36-times",
        "https://indianexpress.com/article/business/market/indian-shares-record-high-after-sensex-breaches-80000-mark-9431868/",
        "https://www.moneycontrol.com/news/business/markets/stock-radar-power-grid-aarti-industries-zydus-lifesciences-ge-power-life-insurance-corporation-sula-vineyards-state-bank-of-india-irb-infrastructure-meson-valves-jtl-industries-in-focus-12766424.html",
        "https://www.ndtvprofit.com/markets/jupiter-wagons-raises-rs-800-crore-from-qip-issue-to-institutional-buyers",
        "https://www.news18.com/business/markets/hcl-tech-announces-interim-dividend-of-rs-12-per-share-for-fy25-check-record-date-8963502.html",
        "https://www.outlookbusiness.com/markets/over-300-returns-in-2024-why-cochin-shipyard-continues-to-shine-at-stock-markets",
        "https://www.thehindu.com/business/markets/markets-decline-in-early-trade/article68380310.ece",
        "https://www.thehindubusinessline.com/markets/stock-markets/brokerage-views-on-dabur-emkay-global-and-dart-insights/article68380231.ece",
        "https://zeenews.india.com/markets/pharma-healthcare-stocks-top-sectoral-gainers-in-trade-2716060.html",
    ],
)
def test_spider_parse(url, snapshot):
    clean_url = re.sub(r"[^\w\-_\. ]", "_", url)
    output_file = f"outputs-parse-test/{clean_url}.json"

    # remove if old data
    if os.path.isfile(output_file):
        os.remove(output_file)

    process = subprocess.run(
        f"scrapy parse {url} -o {output_file} -s SKIP_OUTPUT_URLS=False -s HTTPCACHE_ENABLED=False",
        shell=True,
        capture_output=True,
        text=True,
    )

    assert process.returncode == 0, f"Scrapy command failed: {process.stderr}"

    parsed_json = json.load(open(output_file, "rb"))

    for i in parsed_json:
        # remove fields that change with each run
        del i["scrapy_parsed_at"]
        del i["scrapy_scraped_at"]

    assert parsed_json == snapshot
