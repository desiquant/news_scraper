import json

from ..items import NewsArticleItem, NewsArticleItemLoader
from .base import DailySitemapSpider


class ZeeNewsSpider(DailySitemapSpider):
    name = "zeenews"

    sitemap_frequency = "MS"
    sitemap_patterns = [
        "https://zeenews.india.com/sitemaps/sitemap-{year}-{month}.xml",
    ]
    sitemap_date_formatter = {
        "year": lambda d: d.strftime("%Y"),
        "month": lambda d: d.strftime("%b").lower(),
    }

    sitemap_rules = [(r"/markets/", "parse_article")]

    def parse_article(self, response):
        """
        sample article: https://zeenews.india.com/markets/pharma-healthcare-stocks-top-sectoral-gainers-in-trade-2716060.html
        """

        article = NewsArticleItemLoader(item=NewsArticleItem(), response=response)

        # content
        article.add_css("title", "h1::text")
        article.add_css("description", 'meta[name="description"]::attr(content)')
        article.add_css("author", "span.aaticleauthor_name::text")
        article.add_css("article_html", "div#fullArticle")

        # dates
        ld_data = response.css("script[type='application/ld+json']::text")[2].get()
        ld_json = json.loads(ld_data) if ld_data else {}

        article.add_value("date_published", ld_json.get("datePublished"))
        article.add_value("date_modified", ld_json.get("dateModified"))

        yield article.load_item()
