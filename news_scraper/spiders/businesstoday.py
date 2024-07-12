from ..items import NewsArticleItem, NewsArticleItemLoader
from .base import DailySitemapSpider


class BusinessTodaySpider(DailySitemapSpider):
    name = "businesstoday"

    sitemap_frequency = "1D"
    allowed_domains = ["businesstoday.in"]
    sitemap_patterns = [
        "https://www.businesstoday.in/rssfeeds/date-wise-story-sitemap.xml?yyyy={year}&mm={month}&dd={day}",
    ]

    sitemap_rules = [(r"/markets/", "parse")]

    def parse(self, response):
        """
        sample article: https://www.businesstoday.in/markets/company-stock/story/hdfc-bank-shares-down-8-from-one-year-high-should-you-enter-at-current-levels-436040-2024-07-05
        """

        article = NewsArticleItemLoader(item=NewsArticleItem(), response=response)

        # content
        article.add_css("title", "h1::text")
        article.add_css("description", "h2::text")
        article.add_css("author", "div.brand-detial-main a::text")
        article.add_xpath(
            "article_text", '//div[@id="descriptionStoryId"]/div/p/text()'
        )

        # dates
        article.add_css(
            "date_published",
            'meta[property="article:published_time"]::attr(content)',
        )
        article.add_css(
            "date_modified",
            'meta[property="article:modified_time"]::attr(content)',
        )

        yield article.load_item()
