import json

from ..items import NewsArticleItem, NewsArticleItemLoader
from .base import DailySitemapSpider


class OutlookIndiaSpider(DailySitemapSpider):
    name = "outlookindia"

    sitemap_frequency = "1D"
    allowed_domains = ["outlookindia.com"]
    sitemap_patterns = [
        "https://business.outlookindia.com/sitemap/sitemap-daily-{year}-{month}-{day}.xml",
    ]

    sitemap_rules = [(r"/markets/", "parse")]

    def parse(self, response):
        """
        sample article: https://business.outlookindia.com/markets/over-300-returns-in-2024-why-cochin-shipyard-continues-to-shine-at-stock-markets
        """

        article = NewsArticleItemLoader(item=NewsArticleItem(), response=response)

        # content
        article.add_xpath("title", "//h1//text()")
        article.add_css("description", 'div[data-test-id="subheadline"]::text')
        article.add_css("author", 'a[aria-label="author-name"]::text')
        article.add_xpath("article_text", '//div[@data-test-id="text"]/p/text()')

        # dates
        ld_data = response.css("script[type='application/ld+json']::text")[1].get()
        ld_json = json.loads(ld_data) if ld_data else {}

        article.add_value("date_published", ld_json.get("datePublished"))
        article.add_value("date_modified", ld_json.get("dateModified"))

        yield article.load_item()
