from . base import DailySitemapSpider


class ZeeNewsSpider(DailySitemapSpider):
    name = "zeenews"

    sitemap_frequency = "4W"
    sitemap_patterns = [
        "https://zeenews.india.com/sitemaps/sitemap-{year}-{month}.xml",
    ]
    sitemap_date_formatter = {
        "year": lambda d: d.strftime("%Y"),
        "month": lambda d: d.strftime("%b").lower(),
    }

    sitemap_rules = [(r"/markets/", "parse_article")]

    def parse_article(self, response):
        yield {
            "date": response.css('meta[itemprop="datePublished"]::attr(content)').get(), # TODO
            "title": response.css("h1::text").get(),
            "description": response.css("h2::text").get(),
            "url": response.url,
        }
