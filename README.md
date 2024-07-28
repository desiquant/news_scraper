# DesiQuant News Scraper

A [scrapy](https://github.com/scrapy/scrapy) crawler that scrapes market news from Indian financial news outlets

![test status](https://github.com/desiquant/news_scraper/actions/workflows/test.yml/badge.svg)

> ⚠️ **WARNING**: Work in progress. Will implement breaking frequently. The dataset is not updated everyday. The documentation and code requires more documentation and clarity.

# Data Usage

The data is periodically updated (every 1 hour) and saved to `s3://desiquant/data/news.parquet`. This file can be easily accessed and read as a pandas dataframe as follows:

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

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>url</th>
      <th>title</th>
      <th>article_text</th>
      <th>author</th>
      <th>date_modified</th>
      <th>date_published</th>
      <th>description</th>
      <th>scrapy_parsed_at</th>
      <th>scrapy_scraped_at</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>https://www.moneycontrol.com/news/business/mar...</td>
      <td>Stay stock-specific and maintain strict stop-l...</td>
      <td>It was a historic week (ended July 19) for dom...</td>
      <td>Jigar Patel</td>
      <td>2024-07-21T19:55:46+05:30</td>
      <td>2024-07-21T19:55:46+05:30</td>
      <td>A breach of 24,500 could halt the current mome...</td>
      <td>2024-07-21 17:09:08.064765</td>
      <td>2024-07-21 17:09:07+00:00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>https://www.moneycontrol.com/news/business/mar...</td>
      <td>Wall St ends volatile session lower in afterma...</td>
      <td>US stocks extended their slump on Friday as li...</td>
      <td>Reuters</td>
      <td>2024-07-20T10:17:59+05:30</td>
      <td>2024-07-20T10:17:59+05:30</td>
      <td>The Dow Jones Industrial Average fell 377.49 p...</td>
      <td>2024-07-21 17:09:08.474808</td>
      <td>2024-07-21 17:09:08+00:00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>https://www.moneycontrol.com/news/business/mar...</td>
      <td>Trade Spotlight: How should you trade Federal ...</td>
      <td>The benchmark indices saw profit booking after...</td>
      <td>Sunil Shankar Matkar</td>
      <td>2024-07-11T01:49:05+05:30</td>
      <td>2024-07-11T01:46:54+05:30</td>
      <td>If the Nifty 50 breaks 24,200, the immediate s...</td>
      <td>2024-07-21 17:09:09.444510</td>
      <td>2024-07-21 17:09:08+00:00</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>

  </tbody>
</table>

# Scraper Usage

Run a spider. The outputs are saved to `outputs/moneycontrol.jl` in JSONlines format

```bash
# scrape all market articles from "2010-01-01" till today with
scrapy crawl moneycontrol

# trial run: stops after scraping 10 items. useful for testing purposes
TRIAL_RUN=1 scrapy crawl moneycontrol
```

To view a list of all available spiders:

```bash
scrapy list

# businessstandard
# businesstoday
# economictimes
# financialexpress
# firstpost
# freepressjournal
# indianexpress
# ipfy
# moneycontrol
# ndtvprofit
# news18
# outlookindia
# thehindu
# thehindubusinessline
# zeenews
```

To run all the spiders in production

```bash
# view scraping benchmark tests performed by scrapy
scrapy bench
python run.py
```

Run tests to check if spiders are still working.

```bash
# view the parsed the article
scrapy parse https://www.businesstoday.in/markets/stocks/story/upward-revision-in-eps-estimates-what-analysts-say-on-tcs-q1-results-stock-trading-strategy-436794-2024-07-11

# test all spiders
pip install -e .[test]
pytest
```

# Sitemaps

The sitemaps for each website not always directly available in `robots.txt`. Googling for keywords like `"ndtvprofit.com daily sitemap xml"` seems to retrieve the ones that are not mentioned.

| Publisher                                                       | Sitemap Type     | Sitemap Link                                                                                    |
| --------------------------------------------------------------- | ---------------- | ----------------------------------------------------------------------------------------------- |
| [News 18](https://www.news18.com)                               | Daily Sitemap    | [Link](https://www.news18.com/commonfeeds/v1/eng/sitemap-index.xml)                             |
| [The Hindu](https://www.thehindu.com)                           | Daily Sitemap    | [Link](https://www.thehindu.com/sitemap/archive.xml)                                            |
| [The Hindu Business Line](https://www.thehindubusinessline.com) | Daily Sitemap    | [Link](https://www.thehindubusinessline.com/sitemap/archive.xml)                                |
| [Business Today](https://www.businesstoday.in)                  | Daily Sitemap    | [Link](https://www.businesstoday.in/rssfeeds/date-wise-story-sitemap.xml?yyyy=2023&mm=08&dd=24) |
| [Money Control](https://www.moneycontrol.com)                   | Daily Sitemap    | [Link](https://www.moneycontrol.com/news/sitemap/sitemap-post-2024-07.xml)                      |
| [Business Standard](https://www.business-standard.com)          | Sitemap Index    | [Link](https://www.business-standard.com/sitemap/sitemap-index.xml)                             |
| [Economic Times](https://economictimes.indiatimes.com)          | Monthly Sitemaps | [Link](https://economictimes.indiatimes.com/etstatic/sitemaps/et/sitemap-index.xml)             |
| [Firstpost](https://www.firstpost.com)                          | Daily Sitemap    | [Link](https://www.firstpost.com/commonfeeds/v1/mfp/sitemap/daily/2015-07-08.xml)               |
| [NDTV Profit](https://www.ndtvprofit.com)                       | Daily Sitemap    | [Link](https://www.ndtvprofit.com/sitemap/sitemap-daily-2017-07-08.xml)                         |
| [Free Press Journal](https://www.freepressjournal.in)           | Daily Sitemap    | [Link](https://www.freepressjournal.in/sitemap/sitemap-daily-2015-01-07.xml)                    |
| [Outlook India](https://www.outlookindia.com)                   | Daily Sitemap    | [Link](https://www.outlookindia.com/sitemap/sitemap-daily-2024-07-08.xml)                       |
| [Zee News](https://zeenews.india.com)                           | Monthly Sitemap  | [Link](https://zeenews.india.com/sitemaps/sitemap-2018-feb.xml)                                 |
| [Financial Express](https://www.financialexpress.com)           | Daily Sitemap    | [Link](https://www.financialexpress.com/sitemap.xml?yyyy=2024&mm=07&dd=08)                      |
| [Indian Express](https://indianexpress.com)                     | Daily Sitemap    | [Link](https://indianexpress.com/sitemap.xml?yyyy=2024&mm=07&dd=08)                             |

**More Sources**

The following news websites were in consideration but no daily sitemaps were found. Some effective strategies (requires more research) to iteratively retrieve a list of all articles are mentioned below.

- https://www.livemint.com/api/cms/story/v2/11720327511606 - Check Content Length in Head. TODO: Check for market slug with a smaller query
- https://timesofindia.indiatimes.com/articleshow/81896735.cms - Redirect not showing in head, No sitemap as well.
- https://www.indiainfoline.com/news/top-share-market-news/page/14072 - New articles have no ID in the url. Seems to allow [old articles](https://www.indiainfoline.com/article/x/x-122110400370_1.html) to redirect
- https://in.investing.com/news/a/a-4293269 - Doesn't redirect to actual url

# Notes:

### TODO

- Run the scraper as prefect flow
- Scraping mode - Update/dump
- While running the test, if it fails, prevent scrapy from showing the entire output
- export PYTHONDONTWRITEBYTECODE=1
- pytest failing on few spiders on remote server
- moneycontrol and indianexpress have very aggressive protection. they don't seem to allow usage of even floating ips from hetzner. but ips of brightdata seem to work

### Server Checklist

- Attach floating IPs
- Prevent **pycache**
- Mount volume
