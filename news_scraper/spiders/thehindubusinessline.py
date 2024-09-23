from ..items import NewsArticleItem, NewsArticleItemLoader
from .base import SitemapIndexSpider


class TheHinduBusinessLineSpider(SitemapIndexSpider):
    name = "thehindubusinessline"

    sitemap_type = "daily"
    allowed_domains = ["thehindubusinessline.com"]
    sitemap_patterns = [
        "https://www.thehindubusinessline.com/sitemap/archive/all/{year}{month}{day}_1.xml",
        "https://www.thehindubusinessline.com/sitemap/archive/all/{year}{month}{day}_2.xml",
    ]

    sitemap_rules = [(r"/markets/", "parse"),(r"/economy/", "parse")]

    def parse(self, response):
        """
        sample article: https://www.thehindubusinessline.com/markets/stock-markets/brokerage-views-on-dabur-emkay-global-and-dart-insights/article68380231.ece
        """

        article = NewsArticleItemLoader(item=NewsArticleItem(), response=response)

        # content
        article.add_css("title", "h1::text")
        article.add_css("description", "h2.bl-sub-text::text")
        article.add_css("author", "div.author-name span::text")

        # TODO: href texts are ignored. include them as well
        article.add_xpath("article_text", '//div[@itemprop="articleBody"]/p/text()')

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
