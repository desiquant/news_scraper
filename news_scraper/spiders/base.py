from scrapy.spiders import SitemapSpider, Request
from datetime import date
from typing import Tuple, Callable, Dict, Literal
import pandas as pd


class DailySitemapSpider(SitemapSpider):
    # TODO: the frequency is not being set in months properly
    sitemap_frequency = "4W"
    sitemap_patterns = []
    sitemap_date_formatter: Dict[
        Literal["year", "month", "day"], Callable[[date], str]
    ] = {
        "year": lambda d: d.strftime("%Y"),
        "month": lambda d: d.strftime("%m"),
        "day": lambda d: d.strftime("%d"),
    }

    # TODO: when end date is None, it doesn't seem to work. It should work.
    date_range: Tuple[date | str, date | str] = ("2024-01-01", "2024-03-01")

    def start_requests(self):
        # iterate over date range and process each sitemap
        for dt in pd.date_range(
            start=self.date_range[0],
            end=self.date_range[1],
            freq=self.sitemap_frequency,
        ):
            for sitemap_pattern in self.sitemap_patterns:
                url = sitemap_pattern.format(
                    year=self.sitemap_date_formatter.get("year", lambda x: "")(dt),
                    month=self.sitemap_date_formatter.get("month", lambda x: "")(dt),
                    day=self.sitemap_date_formatter.get("day", lambda x: "")(dt),
                )

                yield Request(url, self._parse_sitemap)
