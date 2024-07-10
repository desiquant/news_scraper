import json
from . base import DailySitemapSpider


class EconomicTimesSpider(DailySitemapSpider):
    name = "economictimes"

    sitemap_frequency = "4W"
    sitemap_patterns = [
        "https://economictimes.indiatimes.com/etstatic/sitemaps/et/{year}-{month}-2.xml",
        "https://economictimes.indiatimes.com/etstatic/sitemaps/et/{year}-{month}-1.xml",
        "https://economictimes.indiatimes.com/etstatic/sitemaps/et/{year}-{month}.xml",
    ]
    sitemap_date_formatter = {
        "year": lambda d: d.strftime("%Y"),
        "month": lambda d: d.strftime("%B"),
    }

    sitemap_rules = [(r"/markets/", "parse_article")]

    def parse_article(self, response):
        script_data = response.css("script[type='application/ld+json']::text")[1].get()
        script_json = json.loads(script_data) if script_data else {}

        yield {
            "date": script_json.get("datePublished"),
            "title": response.css("h1::text").get(),
            "description": response.css("h2::text").get(),
            "url": response.url,
        }
