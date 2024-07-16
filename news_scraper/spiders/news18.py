from ..items import NewsArticleItem, NewsArticleItemLoader
from .base import SitemapIndexSpider


class News18Spider(SitemapIndexSpider):
    name = "news18"

    sitemap_type = "daily"
    allowed_domains = ["news18.com"]
    sitemap_patterns = [
        "https://www.news18.com/commonfeeds/v1/eng/sitemap/daily/{year}-{month}-{day}.xml"
    ]

    sitemap_rules = [(r"/business/", "parse")]

    def parse(self, response):
        """
        sample article: https://www.news18.com/business/markets/hcl-tech-announces-interim-dividend-of-rs-12-per-share-for-fy25-check-record-date-8963502.html
        """

        article = NewsArticleItemLoader(item=NewsArticleItem(), response=response)

        # content
        article.add_css("title", "h1::text")
        article.add_css("description", "h2.short_discription::text")
        article.add_xpath(
            "author", '//span[contains(@class, "article_postby")]//text()'
        )

        # TODO: text in bold are ignored, add this text as well
        article.add_xpath(
            "article_text", '//div[@class="jsx-9ea5c73edc9a77a6"]/p/text()'
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
