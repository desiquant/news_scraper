from . base import DailySitemapSpider


class BusinessTodaySpider(DailySitemapSpider):
    name = "businesstoday"

    sitemap_frequency = "1D"
    sitemap_patterns = [
        "https://www.businesstoday.in/rssfeeds/date-wise-story-sitemap.xml?yyyy={year}&mm={month}&dd={day}",
    ]

    sitemap_rules = [(r"/markets/", "parse_article")]

    def parse_article(self, response):
        yield {
            "date": response.css('meta[property="article:published_time"]::attr(content)').get(),
            "title": response.css("h1::text").get(),
            "description": response.css("h2::text").get(),
            "url": response.url,
        }
