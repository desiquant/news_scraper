# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, Join, MapCompose
from w3lib.html import remove_tags
from datetime import datetime
from scrapy.loader import ItemLoader


class NewsArticleItem(scrapy.Item):
    url = scrapy.Field()

    title = scrapy.Field(input_processor=MapCompose(str.strip))
    description = scrapy.Field(input_processor=MapCompose(str.strip))
    author = scrapy.Field(input_processor=MapCompose(str.strip))

    date_published = scrapy.Field()
    date_modified = scrapy.Field()

    # !TEMP: ignores raw_content
    raw_content = scrapy.Field(output_processor=lambda x: None)
    # raw_content = scrapy.Field(output_processor=Join())
    # text_content = scrapy.Field(
    #     input_processor=MapCompose(remove_tags, str.strip),
    #     output_processor=Join("\n"),
    # )

    # is_paywall = scrapy.Field()

    scrapy_scraped_at = scrapy.Field()
    scrapy_parsed_at = scrapy.Field()


class NewsArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        response = kwargs.get("response")
        if response:
            self.add_value("url", response.url)
            self.add_value(
                "scrapy_scraped_at", response.headers.get("Date").decode("utf-8")
            )
            self.add_value("scrapy_parsed_at", datetime.now().isoformat())
