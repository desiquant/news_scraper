# DesiQuant News Scraper

> A [scrapy](https://github.com/scrapy/scrapy) crawler that scrapes market news from Indian financial news outlets

# Sitemap

https://www.news18.com/story/a-8957928.html - [daily sitemap](https://www.news18.com/commonfeeds/v1/eng/sitemap-index.xml)

https://www.thehindu.com/article68380310.ece - [daily sitemap](https://www.thehindu.com/sitemap/archive.xml)
https://www.thehindubusinessline.com/article68380231.ece - [daily sitemap](https://www.thehindubusinessline.com/sitemap/archive.xml)

https://www.businesstoday.in/story/436192 - [daily sitemap](https://www.businesstoday.in/rssfeeds/date-wise-story-sitemap.xml?yyyy=2023&mm=08&dd=24)

https://www.moneycontrol.com/news/a/b-12764199.html - [daily sitemap](https://www.moneycontrol.com/news/sitemap/sitemap-post-2024-07.xml)

https://www.business-standard.com/a/a-124070800259_1.html - [sitemap index](https://www.business-standard.com/sitemap/sitemap-index.xml)

https://economictimes.indiatimes.com/articleshow/111569297.cms - [monthly sitemaps](https://economictimes.indiatimes.com/etstatic/sitemaps/et/sitemap-index.xml)

https://www.firstpost.com/ - [daily sitemap](https://www.firstpost.com/commonfeeds/v1/mfp/sitemap/daily/2015-07-08.xml)

https://www.ndtvprofit.com/ - [daily_sitemap](https://www.ndtvprofit.com/sitemap/sitemap-daily-2017-07-08.xml)

https://www.freepressjournal.in/ - [daily sitemap](https://www.freepressjournal.in/sitemap/sitemap-daily-2015-01-07.xml)

https://www.outlookindia.com - [daily sitemap](https://www.outlookindia.com/sitemap/sitemap-daily-2024-07-08.xml)

https://zeenews.india.com/2761230 - [monthly sitemap](https://zeenews.india.com/sitemaps/sitemap-2018-feb.xml)

https://www.financialexpress.com/xxx/a-3546452/ - [daily sitemap](https://www.financialexpress.com/sitemap.xml?yyyy=2024&mm=07&dd=08)

https://indianexpress.com/ - [daily sitemap](https://indianexpress.com/sitemap.xml?yyyy=2024&mm=07&dd=08)

# No sitemap

https://www.livemint.com/api/cms/story/v2/11720327511606 - Check Content Length in Head. TODO: Check for market slug with a smaller query

https://timesofindia.indiatimes.com/articleshow/81896735.cms - Redirect not showing in head, No sitemap as well.

https://www.indiainfoline.com/news/top-share-market-news/page/14072 - New articles have no ID in the url. Seems to allow [old articles](https://www.indiainfoline.com/article/x/x-122110400370_1.html) to redirect

https://in.investing.com/news/a/a-4293269 - Doesnt redirect to actual url

# Server Checklist

- Attach floating IPs
- Prevent **pycache**
- Mount volume
