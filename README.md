# DesiQuant News Scraper

> A [scrapy](https://github.com/scrapy/scrapy) crawler that scrapes market news from Indian financial news outlets

# Usage

Run a spider. The outputs are saved to `outputs/moneycontrol.jl` in JSONlines format

```bash
# stop after scraping 10 items. useful for testing purposes
scrapy crawl moneycontrol

# scrape all market articles from "2010-01-01" till today with
TRIAL_RUN=0 scrapy crawl moneycontrol
```

The following websites can be crawled: `moneycontrol`,`thehindu`,`businessstandard`,`news18`,`economictimes`,`indianexpress`,`outlookindia`,`zeenews`,`thehindubusinessline`,`businesstoday`,`freepressjournal`,`firstpost`,`ndtvprofit`,`financialexpress`

To run all the spiders in production

```bash
python run.py
```

Run tests to check if spiders are still working.

```bash
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

# Notes:

### TODO

- Do not cache recent sitemaps
- Run the scraper as prefect flow
- Scraping mode - Update/dump

### Server Checklist

- Attach floating IPs
- Prevent **pycache**
- Mount volume

### More Sources

The following news websites were in consideration but no daily sitemaps were found. Some effective strategies (requires more research) to iteratively retrieve a list of all articles are mentioned below.

- https://www.livemint.com/api/cms/story/v2/11720327511606 - Check Content Length in Head. TODO: Check for market slug with a smaller query
- https://timesofindia.indiatimes.com/articleshow/81896735.cms - Redirect not showing in head, No sitemap as well.
- https://www.indiainfoline.com/news/top-share-market-news/page/14072 - New articles have no ID in the url. Seems to allow [old articles](https://www.indiainfoline.com/article/x/x-122110400370_1.html) to redirect
- https://in.investing.com/news/a/a-4293269 - Doesn't redirect to actual url
