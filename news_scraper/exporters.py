import csv

from scrapy.exporters import CsvItemExporter


class QuotedCsvItemExporter(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        kwargs["quoting"] = csv.QUOTE_ALL  # quote all fields
        super(QuotedCsvItemExporter, self).__init__(*args, **kwargs)
