from ..items import NewsArticleItem, NewsArticleItemLoader
from .base import DailySitemapSpider


class News18Spider(DailySitemapSpider):
    name = "news18"

    sitemap_frequency = "1D"
    sitemap_patterns = [
        "https://www.news18.com/commonfeeds/v1/eng/sitemap/daily/{year}-{month}-{day}.xml"
    ]

    sitemap_rules = [(r"/business/", "parse_article")]

    def parse_article(self, response):
        """
        sample article: https://www.news18.com/business/markets/stocks-to-watch-tcs-nykaa-yes-bank-sbi-tata-elxsi-power-grid-asian-paints-and-others-8961429.html
        """

        article = NewsArticleItemLoader(item=NewsArticleItem(), response=response)

        # content
        article.add_css("title", "h1::text")
        article.add_css("description", "h2.short_discription::text")
        article.add_xpath(
            "author", '//span[contains(@class, "article_postby")]//text()'
        )
        article.add_css("article_html", "article.story_body")

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
