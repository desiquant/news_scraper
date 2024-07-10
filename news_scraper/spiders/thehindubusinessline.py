from . base import DailySitemapSpider


class TheHinduBusinessLineSpider(DailySitemapSpider):
    name = "thehindubusinessline"

    sitemap_frequency = "1D"
    sitemap_patterns = [
        "https://www.thehindubusinessline.com/sitemap/archive/all/{year}{month}{day}_1.xml",
        "https://www.thehindubusinessline.com/sitemap/archive/all/{year}{month}{day}_2.xml",
    ]

    sitemap_rules = [(r"/markets/", "parse_article")]

    def parse_article(self, response):
        yield {
            "date": response.css('meta[itemprop="datePublished"]::attr(content)').get(),
            "title": response.css("h1::text").get(),
            "description": response.css("h2::text").get(),
            "url": response.url,
        }
