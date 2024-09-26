# Notes

## Sitemaps

The sitemaps are usually available in `robots.txt`. If not, you should try to [Google](google.com), [Perplexity](perplexity.ai) for keywords like `"ndtvprofit.com daily sitemap index xml"`. This method helped in retrieving a few sitemap index that are were available otherwise.

#### More Sources

The following news websites were in consideration but no daily sitemaps were found. Some strategies (requires more research) were already explored to iteratively retrieve a list of all articles are mentioned below.

- https://www.livemint.com/api/cms/story/v2/11720327511606 - Check Content Length in Head. TODO: Check for market slug with a smaller query
- https://timesofindia.indiatimes.com/articleshow/81896735.cms - Redirect not showing in head, No sitemap as well.
- https://www.indiainfoline.com/news/top-share-market-news/page/14072 - New articles have no ID in the url. Seems to allow [old articles](https://www.indiainfoline.com/article/x/x-122110400370_1.html) to redirect
- https://in.investing.com/news/a/a-4293269 - Doesn't redirect to actual url

## Scrapy

- **Output Format** - Initially used JSON lines `.jl` format for saving the scraper's output. Unfortunately, parsing JSON lines is very resources intensive while `.csv` is much more efficient. While loading the output as a Pandas DataFrame, a 300 MB of JSON lines takes around 4 GB of RAM to process, whereas CSV has a much lighter memory usage of just around 500 MB.

  This becomes a problem when you have to deploy it to production where you'll have to allocate too much resources for the scraper to function.
