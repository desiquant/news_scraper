from collections import OrderedDict

from scrapy.exporters import JsonLinesItemExporter

""" 
Scrapy requires setting `FEED_EXPORT_FIELDS` if you want to fix a field order on the json item. The ordering is required for a predictable schema while parsing the output from multiple spiders using pandas/dask. Hence we use a custom middleware for this. 
"""


class OrderedJsonLinesItemExporter(JsonLinesItemExporter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def export_item(self, item):
        ordered_item = {field: item.get(field) for field in item.fields.keys()}
        return super().export_item(ordered_item)
