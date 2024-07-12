from ..items import NewsArticleItem, NewsArticleItemLoader
from .base import DailySitemapSpider


class NDTVProfitSpider(DailySitemapSpider):
    name = "ndtvprofit"

    sitemap_frequency = "1D"
    allowed_domains = ["ndtvprofit.com"]
    sitemap_patterns = [
        "https://www.ndtvprofit.com/sitemap/sitemap-daily-{year}-{month}-{day}.xml",
    ]

    sitemap_rules = [(r"/markets/", "parse")]

    def parse(self, response):
        """
        sample article: https://www.ndtvprofit.com/markets/jupiter-wagons-raises-rs-800-crore-from-qip-issue-to-institutional-buyers
        """

        article = NewsArticleItemLoader(item=NewsArticleItem(), response=response)

        # content
        article.add_css("title", "h1::text")
        article.add_css("description", 'meta[property="og:description"]::attr(content)')
        article.add_css("author", 'meta[name="author"]::attr(content)')

        # TODO: missed some href links in article, include that text as well
        article.add_xpath(
            "article_text", '//div[contains(@class,"story-element")]/div/p/text()'
        )

        # dates
        article.add_css(
            "date_published",
            'meta[name="cXenseParse:publishtime"]::attr(content)',
        )
        article.add_css(
            "date_modified",
            'meta[property="article:modified_time"]::attr(content)',
        )

        yield article.load_item()
