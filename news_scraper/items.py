# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from datetime import datetime

from itemloaders.processors import Join, MapCompose, TakeFirst
from scrapy import Field, Item
from scrapy.loader import ItemLoader


class NewsArticleItem(Item):
    url = Field()

    title = Field()
    description = Field()
    author = Field()

    date_published = Field()
    date_modified = Field()

    article_text = Field(output_processor=Join())

    scrapy_scraped_at = Field()
    scrapy_parsed_at = Field()

    paywall = Field()

class NewsArticleItemLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        response = kwargs.get("response")

        if response:
            # add some important fields from response for book keeping purposes
            self.add_value("url", response.url)
            self.add_value(
                "scrapy_scraped_at", response.headers.get("Date").decode("utf-8")
            )
            self.add_value("scrapy_parsed_at", datetime.now().isoformat())

    def load_item(self):
        """
        Modify load_item to set a default "null" value for fields.

        This is to ensure the output has a predictable column structure across all outputs while parsing them as a glob in with dask.
        """
        item = super().load_item()

        for field_name in item.fields:
            if field_name not in item:
                item[field_name] = None
        return item
