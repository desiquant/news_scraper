import json

from ..items import NewsArticleItem, NewsArticleItemLoader
from .base import SitemapIndexSpider


class OutlookIndiaSpider(SitemapIndexSpider):
    name = "outlookindia"

    sitemap_type = "daily"
    allowed_domains = ["outlookbusiness.com"]
    sitemap_patterns = [
        "https://www.outlookbusiness.com/sitemap/sitemap-daily-{year}-{month}-{day}.xml"
    ]

    sitemap_rules = [(r"/markets/", "parse")]

    def parse(self, response):
        """
        sample article: https://www.outlookbusiness.com/markets/over-300-returns-in-2024-why-cochin-shipyard-continues-to-shine-at-stock-markets
        """

        article = NewsArticleItemLoader(item=NewsArticleItem(), response=response)

        # content
        article.add_xpath("title", "//h1//text()")
        article.add_css("description", 'p.subcap-story::text')
        article.add_css("author", 'div.auth-div-button::text')
        article.add_xpath("article_text", '//div[@id="articleBody"]//p/text()')

        article.add_css(
        "date_published",
        'meta[property="article:published_time"]::attr(content)'
        )

        article.add_css(
        "date_modified",
        'meta[property="article:modified_time"]::attr(content)'
        )

        yield article.load_item()
