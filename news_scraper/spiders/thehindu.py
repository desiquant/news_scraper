from ..items import NewsArticleItem, NewsArticleItemLoader
from .base import DailySitemapSpider


class TheHinduSpider(DailySitemapSpider):
    name = "thehindu"

    sitemap_frequency = "1D"
    sitemap_patterns = [
        "https://www.thehindu.com/sitemap/archive/all/{year}{month}{day}_1.xml",
        "https://www.thehindu.com/sitemap/archive/all/{year}{month}{day}_2.xml",
    ]

    sitemap_rules = [(r"/business/markets/", "parse")]

    def parse(self, response):
        """
        sample article: https://www.thehindu.com/business/markets/markets-decline-in-early-trade/article68380310.ece
        """

        article = NewsArticleItemLoader(item=NewsArticleItem(), response=response)

        # content
        article.add_css("title", "h1::text")
        article.add_css("description", "h2.sub-title::text")
        article.add_xpath("author", '//div[@class="author"]//text()')
        article.add_css("article_html", "div.storyline")

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
