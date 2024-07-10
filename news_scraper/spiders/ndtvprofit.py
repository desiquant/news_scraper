from . base import DailySitemapSpider


class NDTVProfitSpider(DailySitemapSpider):
    name = "ndtvprofit"

    sitemap_frequency = "1D"
    sitemap_patterns = [
        "https://www.ndtvprofit.com/sitemap/sitemap-daily-{year}-{month}-{day}.xml",
    ]

    sitemap_rules = [(r"/markets/", "parse_article")]

    def parse_article(self, response):
        yield {
            "date": response.css(
                'meta[name="cXenseParse:publishtime"]::attr(content)'
            ).get(),
            "title": response.css("h1::text").get(),
            "description": response.css("h2::text").get(),
            "url": response.url,
        }
