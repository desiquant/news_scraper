import json

from ..items import NewsArticleItem, NewsArticleItemLoader
from .base import SitemapIndexSpider


class EconomicTimesSpider(SitemapIndexSpider):
    name = "economictimes"

    sitemap_type = "monthly"
    allowed_domains = ["economictimes.indiatimes.com"]
    sitemap_patterns = [
        "https://economictimes.indiatimes.com/etstatic/sitemaps/et/{year}-{month}-2.xml",
        "https://economictimes.indiatimes.com/etstatic/sitemaps/et/{year}-{month}-1.xml",
        "https://economictimes.indiatimes.com/etstatic/sitemaps/et/{year}-{month}.xml",
    ]
    sitemap_date_formatter = {
        "year": lambda d: d.strftime("%Y"),
        "month": lambda d: d.strftime("%B"),
    }

    sitemap_rules = [(r"/markets/", "parse")]

    def parse(self, response):
        """
        sample article: https://economictimes.indiatimes.com/markets/stocks/news/it-stocks-in-focus-ahead-of-june-qtr-results-tcs-cyient-top-buy-which-could-give-15-18-return/articleshow/111569297.cms
        """

        article = NewsArticleItemLoader(item=NewsArticleItem(), response=response)

        # content
        article.add_css("title", "h1::text")
        article.add_css("description", "h2.summary::text")
        article.add_xpath("author", '//div[@class="auth"]//text()')
        article.add_xpath(
            "article_text",
            '//div[@class="artText"]/text() | //div[@class="artText"]/a/text()',
        )
        #paywall
        paywall = "False"
        paywall_element = response.xpath('//h3[@class="paywall_msg"]/@data-free').get()
        paywall_message="You are reading ETPrime's exclusive investment ideas"
        if paywall_element and paywall_message in paywall_element:
            paywall = "True"
        article.add_value("paywall", paywall)

        # dates
        ld_data = response.css("script[type='application/ld+json']::text")[1].get()
        ld_json = json.loads(ld_data) if ld_data else {}

        article.add_value("date_published", ld_json.get("datePublished"))
        article.add_value("date_modified", ld_json.get("dateModified"))

        yield article.load_item()
