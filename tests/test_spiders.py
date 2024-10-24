import json
import multiprocessing
import os
import re
import subprocess
from dotenv import load_dotenv
import pandas as pd
import pytest
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import Settings, get_project_settings
# Load environment variables from .env file
load_dotenv()

def normalize_text(text):
    """Normalize text by collapsing multiple spaces, newlines, etc., into single spaces."""
    if text is None:
        return ""
    return re.sub(r"\s+", " ", text.strip())

from news_scraper.spiders import (
    BusinessStandardSpider,
    BusinessTodaySpider,
    CnbcTv18Spider,
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
    output_file = f"outputs-crawl-test/{spider.name}.csv"

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
            "FEEDS": {output_file: {"format": "csv", "overwrite": True}},
            "HTTPCACHE_ENABLED": False,  # Do not cache requests, # ! TEMP: disable cache
            "LOG_FILE": "test-run.log",  # Prevent log from writing to stdout,
        },
        priority="cmdline",
    )

    if spider.name == "moneycontrol" and bool(os.getenv("PROXY_URL")):
        settings.update(
            {
                "HTTP_PROXY": os.getenv("PROXY_URL"),
                "USE_PROXY": True,  # Set to True to use the proxy
            }
        )
    else:
        # Set an else block to handle other spiders or cases without proxy
        settings.update(
            {
                "USE_PROXY": False,  # Disable proxy usage
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

    if os.path.getsize(output_file) == 0:
        pytest.skip(f"No data scraped by {spider.name}, file {output_file} is empty.")
    df = pd.read_csv(output_file)
    non_paywall_df = df[df["paywall"] == False]
    empty_article_text = non_paywall_df[non_paywall_df['article_text'].isnull()]
    assert empty_article_text.empty, "There are non-paywall articles with empty article_text"

    output_cols = set(df.columns)
    required_cols = {
        "article_text",
        "author",
        "date_modified",
        "date_published",
        "description",
        "scrapy_parsed_at",
        "scrapy_scraped_at",
        "title",
        "url",
        "paywall",
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
        "https://www.thehindu.com/business/Industry/sebi-chief-madhabi-puri-buch-husband-deny-impropriety-allegations/article68638012.ece",
        "https://www.thehindu.com/business/Economy/china-hands-pwc-a-six-month-ban-and-fine-over-audit-of-collapsed-developer-evergrande/article68638086.ece",
        "https://www.thehindubusinessline.com/economy/agri-business/export-demand-lifts-orthodox-tea-prices-at-kochi-auctions/article68637349.ece",
        "https://www.businesstoday.in/industry/aviation/story/delhi-hc-asks-spicejet-and-cmd-ajay-singh-to-pay-rs-100-cr-to-kalanithi-maran-to-prove-bona-fide-395417-2023-08-24",
        "https://www.moneycontrol.com/news/business/companies/ola-electrics-bhavish-aggarwal-responds-to-mapmyindias-notice-defends-ipo-pricing-strategy-12783278.html",
        "https://www.moneycontrol.com/news/business/economy/us-federal-reserve-keeps-key-lending-rate-unchanged-12783729.html",
        "https://www.moneycontrol.com/news/business/earnings/coal-india-q1-net-profit-rises-4-here-are-10-key-points-12783698.html",
        "https://www.business-standard.com/article/companies/hero-motocorp-tax-case-i-t-finds-rs-800-cr-siphoned-off-via-shell-firms-122033101550_1.html",
        "https://www.business-standard.com/article/economy-policy/non-food-credit-growth-accelerates-to-8-in-feb-rbi-data-122033101465_1.html",
        "https://www.ndtvprofit.com/business/trump-s-g-20-ends-with-few-prizes-little-consensus-on-his-goals",
        "https://www.outlookbusiness.com/corporate/blackstone-resumes-talk-for-controlling-stake-in-haldiram-says-report",
        "https://zeenews.india.com/india/pnb-fraud-we-have-businesses-abroad-so-cant-join-investigation-nirav-modi-tells-cbi-2085399.html",
        "https://zeenews.india.com/companies/no-exposure-to-nirav-modi-group-of-companies-icici-bank-2085395.html",
        "https://www.financialexpress.com/business/airlines-aviation-faa-orders-mandatory-inspections-for-2600-boeing-737-planes-over-oxygen-mask-safety-concerns-3547782/",
        "https://www.cnbctv18.com/business/companies/paramount-to-continue-job-cuts-until-skydance-deal-closes-memo-says-19440145.htm",
        "https://www.cnbctv18.com/economy/latest-rbi-klems-data-shows-surprising-jump-in-employment-even-during-pandemic-19440091.htm",
        "https://www.cnbctv18.com/market/godrej-consumer-reports-high-single-digit-organic-volume-growth-in-india-in-q1-19440105.htm",
        "https://economictimes.indiatimes.com/markets/stocks/news/auto-stocks-time-for-a-cool-down-and-also-an-opportunity-6-auto-stocks-with-an-upside-potential-of-up-to-44/articleshow/113926658.cms",
        "https://www.ndtvprofit.com/business/zomato-q2-earnings-shows-it-is-the-new-treasury-trader-in-town",
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

        if "article_text" in i:
            i["article_text"] = normalize_text(i["article_text"])
        # Assert that if paywall is "False", article_text should not be empty
        if i.get("paywall") == "False":
            assert i["article_text"], f"article_text is empty for {i['url']} with paywall False"

    snapshot.assert_match(parsed_json)
