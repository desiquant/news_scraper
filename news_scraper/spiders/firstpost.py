from ..items import NewsArticleItem, NewsArticleItemLoader
from .base import SitemapIndexSpider


class FirstPostSpider(SitemapIndexSpider):
    name = "firstpost"

    sitemap_frequency = "1D"
    allowed_domains = ["firstpost.com"]
    sitemap_patterns = [
        "https://www.firstpost.com/commonfeeds/v1/mfp/sitemap/daily/{year}-{month}-{day}.xml"
    ]

    sitemap_rules = [(r"/india/", "parse")]

    def parse(self, response):
        """
        sample article: https://www.firstpost.com/business/rs-147-5-debited-from-your-sbi-account-heres-why-state-bank-of-india-has-done-this-11792501.html
        """

        article = NewsArticleItemLoader(item=NewsArticleItem(), response=response)

        # content
        article.add_css("title", "h1::text")
        article.add_css("description", "span.less-cont::text")
        article.add_css("author", "div.art-dtls-info a::text")
        article.add_xpath("article_text", '//div[@class="art-content"]/p/text()')

        # dates
        article.add_css(
            "date_published",
            'meta[itemprop="datePublished"]::attr(content)',
        )
        article.add_css(
            "date_modified",
            'meta[itemprop="dateModified"]::attr(content)',
        )

        yield article.load_item()
