from ..items import NewsArticleItem, NewsArticleItemLoader
from .base import SitemapIndexSpider


class IndianExpressSpider(SitemapIndexSpider):
    name = "indianexpress"

    sitemap_type = "daily"
    allowed_domains = ["indianexpress.com"]
    sitemap_patterns = [
        "https://indianexpress.com/sitemap.xml?yyyy={year}&mm={month}&dd={day}"
    ]

    sitemap_rules = [(r"/article/business/", "parse")]

    def parse(self, response):
        """
        sample article: https://indianexpress.com/article/business/market/indian-shares-record-high-after-sensex-breaches-80000-mark-9431868/
        """

        article = NewsArticleItemLoader(item=NewsArticleItem(), response=response)

        # content
        article.add_css("title", "h1::text")
        article.add_css("description", "h2.synopsis::text")
        article.add_css("author", "div.editor a::text")
        article.add_xpath(
            "article_text",
            '//div[@id="pcl-full-content"]/p/text() | //div[contains(@class,"ie-premium-content-block")]/p/text()',
        )

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
