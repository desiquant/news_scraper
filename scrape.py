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
    TheHinduBusinessLineSpider,
    TheHinduSpider,
    ZeeNewsSpider,
    CnbcTv18Spider
)

settings = get_project_settings()

settings.update({"LOG_FILE": "scrape.log"})

process = CrawlerProcess(settings=settings)

process.crawl(BusinessStandardSpider)
process.crawl(BusinessTodaySpider)
process.crawl(EconomicTimesSpider)
process.crawl(FinancialExpressSpider)
process.crawl(FirstPostSpider)
process.crawl(FreePressJournalSpider)
# process.crawl(IndianExpressSpider)
# process.crawl(MoneyControlSpider)
process.crawl(NDTVProfitSpider)
process.crawl(News18Spider)
process.crawl(OutlookIndiaSpider)
process.crawl(TheHinduSpider)
process.crawl(TheHinduBusinessLineSpider)
process.crawl(ZeeNewsSpider)
process.crawl(CnbcTv18Spider)
process.start()
