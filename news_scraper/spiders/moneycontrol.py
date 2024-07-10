from .base import DailySitemapSpider
from ..utils import ua


class MoneyControlSpider(DailySitemapSpider):
    name = "moneycontrol"

    sitemap_frequency = "4W"
    sitemap_patterns = [
        "https://www.moneycontrol.com/news/sitemap/sitemap-post-{year}-{month}.xml",
    ]

    sitemap_rules = [(r"/news/business/markets/", "parse_article")]

    custom_settings = {"USER_AGENT": ua.random}

    def parse_article(self, response):
        yield {
            "date": response.css(
                'meta[property="og:article:published_time"]::attr(content)'
            ).get(),
            "title": response.css("h1::text").get(),
            "description": response.css("h2::text").get(),
            "url": response.url,
        }
