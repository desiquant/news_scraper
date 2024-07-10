from . base import DailySitemapSpider


class FirstPostSpider(DailySitemapSpider):
    name = "firstpost"

    sitemap_frequency = "1D"
    sitemap_patterns = [
        "https://www.firstpost.com/commonfeeds/v1/mfp/sitemap/daily/{year}-{month}-{day}.xml"
    ]

    sitemap_rules = [(r"/india/", "parse_article")]

    def parse_article(self, response):
        yield {
            "date": response.css('meta[itemprop="datePublished"]::attr(content)').get(),
            "title": response.css("h1::text").get(),
            "description": response.css("span.less-cont::text").get(),
            "url": response.url,
        }
