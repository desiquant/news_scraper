from ..items import NewsArticleItem, NewsArticleItemLoader
from ..utils import ua
from .base import DailySitemapSpider


class MoneyControlSpider(DailySitemapSpider):
    name = "moneycontrol"

    sitemap_frequency = "MS"
    allowed_domains = ["moneycontrol.com"]
    sitemap_patterns = [
        "https://www.moneycontrol.com/news/sitemap/sitemap-post-{year}-{month}.xml",
    ]

    sitemap_rules = [(r"/news/business/markets/", "parse")]

    custom_settings = {"USER_AGENT": ua.random}

    def parse(self, response):
        """
        sample article: https://www.moneycontrol.com/news/business/markets/stock-radar-power-grid-aarti-industries-zydus-lifesciences-ge-power-life-insurance-corporation-sula-vineyards-state-bank-of-india-irb-infrastructure-meson-valves-jtl-industries-in-focus-12766424.html
        """

        article = NewsArticleItemLoader(item=NewsArticleItem(), response=response)

        # content
        article.add_css("title", "h1::text")
        article.add_css("description", "h2.article_desc::text")
        article.add_xpath("author", '//div[@class="article_author"]//text()')
        article.add_css("article_html", "div.page_left_wrapper")

        # dates
        article.add_css(
            "date_published",
            'meta[property="og:article:published_time"]::attr(content)',
        )
        article.add_css(
            "date_modified",
            'meta[name="Last-Modified"]::attr(content)',
        )

        yield article.load_item()
