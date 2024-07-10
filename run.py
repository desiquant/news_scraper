from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from news_scraper.spiders import (
    BusinessStandardSpider,
    BusinessTodaySpider,
    EconomicTimesSpider,
    FinancialExpressSpider,
    FirstPostSpider,
    FreePressJournalSpider,
    IndianExpressSpider,
    MoneyControlSpider,
    NDTVProfitSpider,
    News18Spider,
    OutlookIndiaSpider,
    TheHinduSpider,
    TheHinduBusinessLineSpider,
    ZeeNewsSpider,
)


process = CrawlerProcess(settings=get_project_settings())

process.crawl(BusinessStandardSpider)
process.crawl(BusinessTodaySpider)
process.crawl(EconomicTimesSpider)
process.crawl(FinancialExpressSpider)
process.crawl(FirstPostSpider)
process.crawl(FreePressJournalSpider)
process.crawl(IndianExpressSpider)
process.crawl(MoneyControlSpider)
process.crawl(NDTVProfitSpider)
process.crawl(News18Spider)
process.crawl(OutlookIndiaSpider)
process.crawl(TheHinduSpider)
process.crawl(TheHinduBusinessLineSpider)
process.crawl(ZeeNewsSpider)

process.start()
