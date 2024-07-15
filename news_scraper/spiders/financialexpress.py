from ..items import NewsArticleItem, NewsArticleItemLoader
from .base import SitemapIndexSpider


class FinancialExpressSpider(SitemapIndexSpider):
    name = "financialexpress"

    sitemap_frequency = "1D"
    allowed_domains = ["financialexpress.com"]
    sitemap_patterns = [
        "https://www.financialexpress.com/sitemap.xml?yyyy={year}&mm={month}&dd={day}"
    ]

    sitemap_rules = [(r"/market/", "parse")]

    def parse(self, response):
        """
        sample article: https://www.financialexpress.com/market/will-markets-crash-ahead-of-budget-is-it-the-right-time-to-book-profitsnbsp-check-key-nifty-levels-to-watch-3549556/
        """

        article = NewsArticleItemLoader(item=NewsArticleItem(), response=response)

        # content
        article.add_css("title", "h1::text")
        article.add_css("description", "h2.heading-four::text")
        article.add_css("author", 'meta[itemprop="author"]::attr(content)')
        article.add_xpath("article_text", '//div[@id="pcl-full-content"]/p/text()')

        # dates
        article.add_css(
            "date_published",
            'meta[itemprop="article:published_time"]::attr(content)',
        )
        article.add_css(
            "date_modified",
            'meta[itemprop="article:modified_time"]::attr(content)',
        )

        yield article.load_item()
