from . base import DailySitemapSpider


class OutlookIndiaSpider(DailySitemapSpider):
    name = "outlookindia"

    sitemap_frequency = "1D"
    sitemap_patterns = [
        "https://business.outlookindia.com/sitemap/sitemap-daily-{year}-{month}-{day}.xml",
    ]

    sitemap_rules = [(r"/markets/", "parse_article")]

    def parse_article(self, response):
        yield {
            "date": response.css('meta[itemprop="datePublished"]::attr(content)').get(), # TODO
            "title": response.css("h1::text").get(),
            "description": response.css("h2::text").get(),
            "url": response.url,
        }
