from ..items import NewsArticleItem, NewsArticleItemLoader
from ..utils import ua
from .base import DailySitemapSpider


class BusinessStandardSpider(DailySitemapSpider):
    name = "businessstandard"

    sitemap_frequency = "4W"
    sitemap_patterns = [
        "https://www.business-standard.com/sitemap/{year}-{month}-1.xml",
    ]
    sitemap_date_formatter = {
        "year": lambda d: d.strftime("%Y"),
        "month": lambda d: d.strftime("%B").lower(),
    }

    sitemap_rules = [(r"/markets/", "parse_article")]

    custom_settings = {"USER_AGENT": ua.random}

    def parse_article(self, response):
        article = NewsArticleItemLoader(item=NewsArticleItem(), response=response)

        # content
        article.add_css("title", "h1.stryhdtp::text")
        article.add_css("description", "h2.strydsc::text")
        article.add_css("author", "span.MainStory_dtlauthinfo__u_CUx span::text")
        article.add_css("raw_content", "div.storydetail")

        # dates
        article.add_css(
            "date_published",
            'meta[property="article:published_time"]::attr(content)',
        )
        article.add_css(
            "date_modified",
            'meta[http-equiv="Last-Modified"]::attr(content)',
        )

        yield article.load_item()
