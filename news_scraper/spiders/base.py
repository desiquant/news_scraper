from datetime import date
from typing import Callable, Dict, Literal, Tuple

import pandas as pd
from scrapy.spiders import Request, SitemapSpider

from ..utils import yesterday


class SitemapIndexSpider(SitemapSpider):
    sitemap_frequency = "MS"  # MS -> Month Start
    sitemap_patterns = []
    sitemap_date_formatter: Dict[
        Literal["year", "month", "day"], Callable[[date], str]
    ] = {
        "year": lambda d: d.strftime("%Y"),
        "month": lambda d: d.strftime("%m"),
        "day": lambda d: d.strftime("%d"),
    }

    date_range: Tuple[date | str, date | str] = ("2020-01-01", yesterday)

    def start_requests(self):
        sitemap_dates = pd.date_range(
            start=self.date_range[0],
            end=self.date_range[1],
            freq=self.sitemap_frequency,
        )[::-1]

        sitemaps_processed = 0
        limit_sitemaps = self.settings.getint("CLOSESPIDER_ITEMCOUNT", 0) > 0

        # iterate over date range and process each sitemap
        for dt in sitemap_dates:
            for sitemap_pattern in self.sitemap_patterns:
                url = sitemap_pattern.format(
                    year=self.sitemap_date_formatter.get("year", lambda x: "")(dt),
                    month=self.sitemap_date_formatter.get("month", lambda x: "")(dt),
                    day=self.sitemap_date_formatter.get("day", lambda x: "")(dt),
                )

                yield Request(url, self._parse_sitemap, meta={"dont_cache": True})

                sitemaps_processed += 1

                # limit sitemaps if item limit is set on scraper
                if limit_sitemaps and sitemaps_processed >= 3:
                    self.logger.info("Sitemap limit hit!")
                    return
