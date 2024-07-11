from ..items import NewsArticleItem, NewsArticleItemLoader
from .base import DailySitemapSpider


class TheHinduBusinessLineSpider(DailySitemapSpider):
    name = "thehindubusinessline"

    sitemap_frequency = "1D"
    allowed_domains = ["thehindubusinessline.com"]
    sitemap_patterns = [
        "https://www.thehindubusinessline.com/sitemap/archive/all/{year}{month}{day}_1.xml",
        "https://www.thehindubusinessline.com/sitemap/archive/all/{year}{month}{day}_2.xml",
    ]

    sitemap_rules = [(r"/markets/", "parse")]

    def parse(self, response):
        """
        sample article: https://www.thehindubusinessline.com/markets/stock-markets/brokerage-views-on-dabur-emkay-global-and-dart-insights/article68380231.ece
        """

        article = NewsArticleItemLoader(item=NewsArticleItem(), response=response)

        # content
        article.add_css("title", "h1::text")
        article.add_css("description", "h2.bl-sub-text::text")
        article.add_css("author", "div.author-name span::text")
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
