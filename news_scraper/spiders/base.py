from datetime import date
from typing import Callable, Dict, Literal, Tuple

import pandas as pd
from scrapy.spiders import Request, SitemapSpider

from ..utils import yesterday


class DailySitemapSpider(SitemapSpider):
    sitemap_frequency = "MS"  # MS -> Month Start
    sitemap_patterns = []
    sitemap_date_formatter: Dict[
        Literal["year", "month", "day"], Callable[[date], str]
    ] = {
        "year": lambda d: d.strftime("%Y"),
        "month": lambda d: d.strftime("%m"),
        "day": lambda d: d.strftime("%d"),
    }

    date_range: Tuple[date | str, date | str] = ("2010-01-01", yesterday)

    def start_requests(self):
        # iterate over date range and process each sitemap
        for dt in reversed(
            pd.date_range(
                start=self.date_range[0],
                end=self.date_range[1],
                freq=self.sitemap_frequency,
            )
        ):
            for sitemap_pattern in self.sitemap_patterns:
                url = sitemap_pattern.format(
                    year=self.sitemap_date_formatter.get("year", lambda x: "")(dt),
                    month=self.sitemap_date_formatter.get("month", lambda x: "")(dt),
                    day=self.sitemap_date_formatter.get("day", lambda x: "")(dt),
                )

                yield Request(url, self._parse_sitemap)
