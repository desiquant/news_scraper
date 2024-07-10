from . base import DailySitemapSpider


class IndianExpressSpider(DailySitemapSpider):
    name = "indianexpress"

    sitemap_frequency = "1D"
    sitemap_patterns = [
        "https://indianexpress.com/sitemap.xml?yyyy={year}&mm={month}&dd={day}"
    ]

    sitemap_rules = [(r"/article/business/", "parse_article")]

    def parse_article(self, response):
        yield {
            "date": response.css('meta[itemprop="datePublished"]::attr(content)').get(),
            "title": response.css("h1::text").get(),
            "description": response.css("h2::text").get(),
            "url": response.url,
        }
