from . base import DailySitemapSpider


class FreePressJournalSpider(DailySitemapSpider):
    name = "freepressjournal"

    sitemap_frequency = "1D"
    sitemap_patterns = [
        "https://www.freepressjournal.in/sitemap/sitemap-daily-{year}-{month}-{day}.xml",
    ]

    sitemap_rules = [(r"/business/", "parse_article")]

    def parse_article(self, response):
        yield {
            "date": response.css('meta[itemprop="datePublished"]::attr(content)').get(),
            "title": response.css("h1::text").get(),
            "description": response.css("h2::text").get(),
            "url": response.url,
        }
