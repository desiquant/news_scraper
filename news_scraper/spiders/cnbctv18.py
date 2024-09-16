from ..items import NewsArticleItem, NewsArticleItemLoader
from .base import SitemapIndexSpider

class CnbcTv18Spider(SitemapIndexSpider):
    name = "cnbctv18"
    
    sitemap_type = "daily"
    allowed_domains = ["cnbctv18.com"]
    sitemap_patterns = [
        "https://www.cnbctv18.com/commonfeeds/v1/cne/sitemap/daily/{year}-{month}-{day}.xml",
    ]
    
    sitemap_rules = [(r"/market/", "parse")]
    
    def parse(self, response):
        """
        Sample article: https://www.cnbctv18.com/market/stock-market-live-updates-nifty-sensex-today-tata-steel-adani-hpcl-bpcl-route-mobile-oil-share-price-liveblog-19474899.htm
        """
        
        article = NewsArticleItemLoader(item=NewsArticleItem(), response=response)
        
        # Content
        article.add_css("title", "h1.schema-headline-target::text")
        article.add_css("description", "h2.schema-summary-target::text")
        article.add_xpath(
            "author", "//div[contains(@class, 'narticle-author')]//span[contains(@class, 'nauthor-name')]/span[contains(@class, 'jsx-61453e8285f2673c')]//text()"
        )
        article.add_xpath(
            "article_text", "//div[contains(@class, 'narticle-data')]//div[contains(@class, 'articleWrap')]//text()"
        )
        
        # Dates
        article.add_css(
            "date_published", "meta[property='article:published_time']::attr(content)"
        )
        article.add_css(
            "date_modified", "meta[property='article:modified_time']::attr(content)"
        )
        
        yield article.load_item()
