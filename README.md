# DesiQuant: News Scraper

A [scrapy](https://github.com/scrapy/scrapy) crawler that scrapes market news from Indian financial news outlets
A [scrapy](https://github.com/scrapy/scrapy) crawler that scrapes market news from Indian financial news outlets

![test status](https://github.com/desiquant/news_scraper/actions/workflows/test.yml/badge.svg)

| Publisher                                                       | Sitemap Type                                                                                     |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| [News 18](https://www.news18.com)                               | [Daily](https://www.news18.com/commonfeeds/v1/eng/sitemap/daily/2024-09-13.xml)                  |
| [The Hindu](https://www.thehindu.com)                           | [Daily](https://www.thehindu.com/sitemap/archive/all/20240913_1.xml)                             |
| [The Hindu Business Line](https://www.thehindubusinessline.com) | [Daily](https://www.thehindubusinessline.com/sitemap/archive/all/20240913_1.xml)                 |
| [Business Today](https://www.businesstoday.in)                  | [Daily](https://www.businesstoday.in/rssfeeds/date-wise-story-sitemap.xml?yyyy=2023&mm=08&dd=24) |
| [Money Control](https://www.moneycontrol.com)                   | [Monthly](https://www.moneycontrol.com/news/sitemap/sitemap-post-2024-07.xml)                    |
| [Business Standard](https://www.business-standard.com)          | [Monthly](https://www.business-standard.com/sitemap/2022-march-1.xml)                            |
| [Economic Times](https://economictimes.indiatimes.com)          | [Monthly](https://economictimes.indiatimes.com/etstatic/sitemaps/et/2024-August-1.xm)            |
| [Firstpost](https://www.firstpost.com)                          | [Daily](https://www.firstpost.com/commonfeeds/v1/mfp/sitemap/daily/2015-07-08.xml)               |
| [NDTV Profit](https://www.ndtvprofit.com)                       | [Daily](https://www.ndtvprofit.com/sitemap/sitemap-daily-2017-07-08.xml)                         |
| [Free Press Journal](https://www.freepressjournal.in)           | [Daily](https://www.freepressjournal.in/sitemap/sitemap-daily-2015-01-07.xml)                    |
| [Outlook India](https://www.outlookindia.com)                   | [Daily](https://www.outlookindia.com/sitemap/sitemap-daily-2024-07-08.xml)                       |
| [Zee News](https://zeenews.india.com)                           | [Monthly](https://zeenews.india.com/sitemaps/sitemap-2018-feb.xml)                               |
| [Financial Express](https://www.financialexpress.com)           | [Daily](https://www.financialexpress.com/sitemap.xml?yyyy=2024&mm=07&dd=08)                      |
| [Indian Express](https://indianexpress.com)                     | [Daily](https://indianexpress.com/sitemap.xml?yyyy=2024&mm=07&dd=08)                             |

## Data Usage

You can readily consume the data without setting up any infrastructure. The data is publicly accessible and updated every 1 hour. <u>**The entire data dump is around 5 GB**</u> and increases by ~10 MB everyday.

##### Data Files

The entire consolidated data is accessible at `s3://desiquant/data/news.parquet`

The individual news publisher data files are accessible at `s3://desiquant/data/news/cnbctv18.jl`. To view a list of all available publishers you can check out [below](#local-development)

##### Pandas Usage

```python
import s3fs
import pandas as pd

df = pd.read_parquet("s3://desiquant/data/news.parquet", storage_options={
    "key": "sceN1eFOJQmBIWHNEMd8",
    "secret": "w1BERx7F6LTe87sk9K9deoBcfYXNCwlol5xcLeev",
    "endpoint_url": "http://data.desiquant.com:9000",
})
df
```

##### Data Preview

| title                                                           | author        | description                                                                | url                                                                                                                                                       | article_text                                                                       | date_modified             | date_published            | scrapy_scraped_at             | scrapy_parsed_at           |
| --------------------------------------------------------------- | ------------- | -------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ------------------------- | ------------------------- | ----------------------------- | -------------------------- |
| These smallcaps gain 10-50% despite the underperformance...     | Rakesh Patil  | A sustainable plunge below 24500 is likely to provide some more respite... | https://www.moneycontrol.com/news/business/markets/these-smallcaps-gain-10-50-despite-broader-indices-underperform-12773539.html                          | The broader indices underperformed the main indices...                             | 2024-07-20T12:07:07+05:30 | 2024-07-20T12:05:48+05:30 | Sun, 21 Jul 2024 17:09:08 GMT | 2024-07-21T17:12:27.979827 |
| Budget Buzz: Quantum AMC’s Chirag Mehta expects a populist...   | Anishaa Kumar | Mehta says that the impact of earlier government spends has been skewed... | https://www.moneycontrol.com/news/business/markets/budget-buzz-quantum-amcs-chirag-mehta-expects-a-populist-budget-airs-his-mf-tax-wishlist-12773526.html | Talking about the upcoming budget, Quantum AMC's Chief Investment Officer (CIO)... | 2024-07-20T13:18:33+05:30 | 2024-07-20T13:17:21+05:30 | Sun, 21 Jul 2024 17:12:27 GMT | 2024-07-21T17:12:28.985228 |
| Digital curbs impact Kotak Bank's unsecured loan book growth... | Lovisha Darad | Kotak Mahindra Bank reported a 20 basis points (bps) sequential drop...    | https://www.moneycontrol.com/news/business/markets/digital-curbs-impact-kotak-banks-unsecured-loan-book-growth-margin-in-q1fy25-12773719.html             | As Kotak Mahindra Bank marks three months of facing a ban...                       | 2024-07-20T18:55:10+05:30 | 2024-07-20T18:55:10+05:30 | Sun, 21 Jul 2024 17:12:27 GMT | 2024-07-21T17:12:29.051476 |

## Local Development

#### Setup

Install all python dependencies

```bash
pip install -e . # editable mode
```

To scrape all market articles from [MoneyControl](https://moneycontrol.com), you can run the following spider. By default, only the articles from the **last week** are scraped.

```bash
scrapy crawl moneycontrol
```

That's it! You can now view the scraped news articles at `data/outputs/moneycontrol.jl`. The articles are saved in [JSON Lines](https://jsonlines.org/examples/) format in a structured format like:

```json
{
  "article_text": "As Kotak Mahindra Bank marks three months of facing a ban on digital onboarding of customers, the private sector lender highlighted the impact the ban had on its unsecured loan book growth and margins during the April-June quarter (Q1FY25). \"As I mentioned in the last quarter's results, the RBI order would affect our 811 and credit card businesses. This has had some impact on unsecured book growth and consequently on net interest margin (NIM). However, we believe that when the embargo is lifted, we will come out even more strongly. If you take out the impact on the unsecured businesses and 811, the rest of the business grew very well,\" the bank's management said in their earnings conference call. In the June-ended quarter, Kotak Mahindra Bank reported a 20 basis points (bps) sequential drop in its unsecured loan book growth to 11.6 percent from 11.8 percent. On the other hand, NIM remained flat quarter-on-quarter at 5.02 percent in Q1FY24, but was down 55 bps year-on-year from 5.57 percent in Q1FY23. On April 24, 2024, the Reserve Bank of India barred Kotak Mahindra Bank from taking on new customers via its online and mobile banking channels and from issuing new credit cards. The central bank took this action after examining the country's fourth-largest private lender's IT systems in 2022 and 2023 and finding concerns that Kotak failed to adequately address information technology-related drawbacks. When asked about the progress made in improving its IT systems, Kotak Bank said they are committed to completing the process efficiently. \"It is hard to predict when the RBI will approve the complete overhaul of our technology systems. But, we remain committed to finishing everything and are working on this with great determination. We will continue to perfect our tech systems with incredible gusto and mitigate this impact as soon as possible,\" the management stated. ",
  "author": "Lovisha Darad",
  "date_modified": "2024-07-20T18:55:10+05:30",
  "date_published": "2024-07-20T18:55:10+05:30",
  "description": "Kotak Mahindra Bank reported a 20 basis points (bps) sequential drop in its unsecured loan book growth to 11.6 percent  in Q1FY25 from 11.8 percent",
  "scrapy_parsed_at": "2024-07-21T17:12:29.051476",
  "scrapy_scraped_at": "Sun, 21 Jul 2024 17:12:27 GMT",
  "title": "Digital curbs impact Kotak Bank's unsecured loan book growth, margin in Q1FY25",
  "url": "https://www.moneycontrol.com/news/business/markets/digital-curbs-impact-kotak-banks-unsecured-loan-book-growth-margin-in-q1fy25-12773719.html"
}
```

#### Testing

The tests check that data is correctly pulled from news article webpages. When a website structure changes, the tests should ideally fail so that we can promptly make updates to the spiders.

```bash
pip install .[test] # install all test deps
pytest # test all spiders
```

#### Scrapy CLI

Here are some useful built-in scrapy commands:

```bash
scrapy list # view a list of all available spiders
scrapy bench # view scraping benchmark tests performed by scrapy

# view the parsed article output
scrapy parse https://www.businesstoday.in/markets/stocks/story/upward-revision-in-eps-estimates-what-analysts-say-on-tcs-q1-results-stock-trading-strategy-436794-2024-07-11
```

## Production

Deploying the spider in production involves the following steps:

- **Configure Settings**: All the relevant data generated by scrapy is stored in the `data` folder which can be set in [scrapy.cfg](scrapy.cfg). Moreover, the following custom scrapy settings are available in [settings.py](news_scraper/settings.py#L10)

| Setting            | Description                                                                          | Default                              |
| ------------------ | ------------------------------------------------------------------------------------ | ------------------------------------ |
| `SKIP_OUTPUT_URLS` | Skips fetching and parsing of articles that already exist in the output of a spider. | `True`                               |
| `USE_FLOATING_IPS` | Uses all available floating IPs on `eth0` to prevent IP-based blocks while scraping. | `True`                               |
| `DATE_RANGE`       | Gathers and scrapes articles within the specified date range from the sitemap.       | `(datetime.today(), datetime.now())` |

- **Infrastructure**:

  - Create a server.
  - Mount a 100 GB+ volume to save output and cache data. Point the above mentioned `data` directory to this volume.
  - Attach 40+ floating IPs. These IPs will automatically be used by the scraper.

- **Run Scraper** - Start the scraping by running `python scrape.py`. The logs are saved at `scrape.log`

- **Verify Output** - You should see the articles saved in `data/outputs` folder. Timely check the `scrape.log` to verify that the scraper is running as expected. _That's it!_

You also can seamlessly [integrate scrapy](https://docs.scrapy.org/en/1.8/topics/practices.html#run-from-script) into an ETL pipeline with frameworks like [Prefect](https://github.com/PrefectHQ/prefect) to maintain an updated dataset.
