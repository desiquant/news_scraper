from ..items import NewsArticleItem, NewsArticleItemLoader
from ..utils import ua
from .base import SitemapIndexSpider


class MoneyControlSpider(SitemapIndexSpider):
    name = "moneycontrol"

    sitemap_type = "monthly"
    allowed_domains = ["moneycontrol.com"]
    sitemap_patterns = [
        "https://www.moneycontrol.com/news/sitemap/sitemap-post-{year}-{month}.xml",
    ]

    sitemap_rules = [(r"/news/business/markets/", "parse"),(r"/news/business/economy/", "parse"),(r"/news/business/companies/", "parse"),(r"/news/business/earnings/", "parse")]

    custom_settings = {"USER_AGENT": ua.random}

    def parse(self, response):
        """
        sample article: https://www.moneycontrol.com/news/business/markets/stock-radar-power-grid-aarti-industries-zydus-lifesciences-ge-power-life-insurance-corporation-sula-vineyards-state-bank-of-india-irb-infrastructure-meson-valves-jtl-industries-in-focus-12766424.html
        """
        
        if response.url == "https://www.moneycontrol.com/news/":
            self.logger.info(f"Ignoring invalid URL: {response.url}")
            return  # Skip parsing for invalid URLs

        # Check if the meta tag contains the word "podcast" and skip if true
        meta_content = response.xpath('//meta[@property="og:type"]/@content').get()
        if meta_content and "podcast" in meta_content.lower():
            self.logger.info(f"Skipping podcast URL: {response.url}")
            return  # Skip parsing for podcast URLs

        article = NewsArticleItemLoader(item=NewsArticleItem(), response=response)

        # content
        article.add_css("title", "h1::text")
        article.add_css("description", "h2.article_desc::text")
        article.add_xpath("author", '//div[@class="article_author"]//text()')
        article.add_xpath(
            "article_text",
            (
                '//div[@id="contentdata"]/p/text() |'
                #handling livefeed articles
                '//ul[@class="liveblog_list live-blog liveBlogListInfo"]//li[@class="blog-commmand"]/div/h3[@class="Blue_text"]//text() | '
                '//ul[@class="liveblog_list live-blog liveBlogListInfo"]//li[@class="blog-commmand"]/div/div[@itemprop="articleBody"]//text()'
            )
        )
        paywall = "False"
        paywall_element = response.xpath('//div[@class="sub_prosection proRequest"]').get()
        paywall_message = "Unlock this article at ₹1"
        if paywall_element and (paywall_message in paywall_element):
            paywall = "True"
        article.add_value("paywall", paywall)

        # dates
        article.add_css(
            "date_published",
            'meta[property="og:article:published_time"]::attr(content)',
        )
        article.add_css(
            "date_modified",
            'meta[name="Last-Modified"]::attr(content)',
        )

        yield article.load_item()
