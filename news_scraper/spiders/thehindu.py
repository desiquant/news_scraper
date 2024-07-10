from . base import DailySitemapSpider


class TheHinduSpider(DailySitemapSpider):
    name = "thehindu"

    sitemap_frequency = "1D"
    sitemap_patterns = [
        "https://www.thehindu.com/sitemap/archive/all/{year}{month}{day}_1.xml",
        "https://www.thehindu.com/sitemap/archive/all/{year}{month}{day}_2.xml",
    ]

    sitemap_rules = [(r"/business/markets/", "parse_article")]

    def parse_article(self, response):
        yield {
            "date": response.css('meta[itemprop="datePublished"]::attr(content)').get(),
            "title": response.css("h1::text").get(),
            "description": response.css("h2::text").get(),
            "url": response.url,
        }
