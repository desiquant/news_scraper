from . base import DailySitemapSpider


class FinancialExpressSpider(DailySitemapSpider):
    name = "financialexpress"

    sitemap_frequency = "1D"
    sitemap_patterns = [
        "https://www.financialexpress.com/sitemap.xml?yyyy={year}&mm={month}&dd={day}"
    ]

    sitemap_rules = [(r"/market/", "parse_article")]

    def parse_article(self, response):
        yield {
            "date": response.css('meta[itemprop="datePublished"]::attr(content)').get(),
            "title": response.css("h1::text").get(),
            "description": response.css("h2::text").get(),
            "url": response.url,
        }
