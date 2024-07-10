from . base import DailySitemapSpider


class News18Spider(DailySitemapSpider):
    name = "news18"

    sitemap_frequency = "1D"
    sitemap_patterns = [
        "https://www.news18.com/commonfeeds/v1/eng/sitemap/daily/{year}-{month}-{day}.xml"
    ]

    sitemap_rules = [(r"/business/", "parse_article")]

    def parse_article(self, response):
        yield {
            "date": response.css('meta[itemprop="datePublished"]::attr(content)').get(),
            "title": response.css("h1::text").get(),
            "description": response.css("h2::text").get(),
            "url": response.url,
        }
