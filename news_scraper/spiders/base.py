from datetime import date
from pathlib import Path
from typing import Callable, Dict, Literal

import pandas as pd
from scrapy.spiders import Request, SitemapSpider
from scrapy.utils.project import data_path

from ..utils import get_spider_output


class SitemapIndexSpider(SitemapSpider):
    sitemap_type: Literal["daily", "monthly", "yearly"] = "monthly"
    sitemap_patterns = []
    sitemap_date_formatter: Dict[
        Literal["year", "month", "day"], Callable[[date], str]
    ] = {
        "year": lambda d: d.strftime("%Y"),
        "month": lambda d: d.strftime("%m"),
        "day": lambda d: d.strftime("%d"),
    }

    # TODO: can make make a pull request to allow property decorator for custom_settings instead of dict.
    @classmethod
    def update_settings(cls, settings):
        """
        Overrides the default update_settings class to modify settings that include dynamic values from the spider and whose values can also be used in the middleware for eg. getting the output path of each spider.
        """

        # we are using data_path to colocate outputs and httpcache
        output_file = Path(data_path("outputs", createdir=True)) / f"{cls.name}.jl"

        # we are setting the output filepath here and not in settings.py so that we have a static filepath
        custom_settings = cls.custom_settings or {}
        custom_settings.update(
            dict(
                FEEDS={
                    output_file: {
                        "format": "jsonlines",
                        "store_empty": False,
                    }
                }
            )
        )

        settings.update(custom_settings, priority="spider")

    def start_requests(self):
        if self.sitemap_type == "daily":
            sitemap_frequency = pd.DateOffset(days=1)
        elif self.sitemap_type == "monthly":
            sitemap_frequency = pd.DateOffset(months=1)
        elif self.sitemap_type == "yearly":
            sitemap_frequency = pd.DateOffset(years=1)
        else:
            raise NotImplementedError(self.sitemap_type)

        # calculate appropriate date_range
        date_range = self.settings.getlist("DATE_RANGE")

        # restrict date_range based on existing scraped data.
        if self.settings.getbool("SKIP_OUTPUT_URLS"):
            for output_file, _ in self.settings.getdict("FEEDS").items():
                df = get_spider_output(output_file)

                if df.empty:
                    continue

                # update starting date from last published/modified article
                date_range[0] = max(
                    df["date_modified"].max(),
                    df["date_published"].max(),
                    date_range[0],
                )
                self.logger.info(
                    "Already scraped upto %s in: %s" % (date_range[0], output_file)
                )

        # restrict sitemap date range
        # note: the below ensures at least one sitemap is always scraped
        sitemap_dates = pd.date_range(
            start=pd.Timestamp(date_range[0]).normalize(),
            end=pd.Timestamp(date_range[1]).normalize(),
            freq=sitemap_frequency,
        )[::-1]

        self.logger.info("scraping DATE_RANGE: %s", date_range)
        self.logger.info("scraping sitemaps: %s", sitemap_dates)

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
