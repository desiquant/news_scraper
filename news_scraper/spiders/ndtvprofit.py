from ..items import NewsArticleItem, NewsArticleItemLoader
from .base import DailySitemapSpider


class NDTVProfitSpider(DailySitemapSpider):
    name = "ndtvprofit"

    sitemap_frequency = "1D"
    sitemap_patterns = [
        "https://www.ndtvprofit.com/sitemap/sitemap-daily-{year}-{month}-{day}.xml",
    ]

    sitemap_rules = [(r"/markets/", "parse_article")]

    def parse_article(self, response):
        """
        sample article: https://www.ndtvprofit.com/markets/stocks-to-watch-asian-paints-sula-vineyards-glenmark-pharma-power-grid
        """

        article = NewsArticleItemLoader(item=NewsArticleItem(), response=response)

        # content
        article.add_css("title", "h1::text")
        article.add_css("description", 'meta[property="og:description"]::attr(content)')
        article.add_css("author", 'meta[name="author"]::attr(content)')
        article.add_css(
            "article_html", "div.story-base-template-m__left-sidebar__hvXQs"
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
