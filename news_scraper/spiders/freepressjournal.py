from ..items import NewsArticleItem, NewsArticleItemLoader
from .base import SitemapIndexSpider


class FreePressJournalSpider(SitemapIndexSpider):
    name = "freepressjournal"

    sitemap_frequency = "1D"
    allowed_domains = ["freepressjournal.in"]
    sitemap_patterns = [
        "https://www.freepressjournal.in/sitemap/sitemap-daily-{year}-{month}-{day}.xml",
    ]

    sitemap_rules = [(r"/business/", "parse")]

    def parse(self, response):
        """
        sample article: https://www.freepressjournal.in/business/sbi-raises-10000-cr-via-sixth-infrastructure-bond-issuance-at-736-coupon-rate-oversubscribed-36-times
        """

        article = NewsArticleItemLoader(item=NewsArticleItem(), response=response)

        # content
        article.add_css("title", "h1::text")
        article.add_css("description", "h2#heading-2::text")
        article.add_css("author", "a.author-name::text")
        article.add_xpath("article_text", '//article[@id="fjp-article"]/p/text()')

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
