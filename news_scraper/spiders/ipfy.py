import scrapy


class IpfySpider(scrapy.Spider):
    name = "ipfy"
    start_urls = ["https://api.ipify.org/"]
    
    custom_settings = {
        "HTTPCACHE_ENABLED": False
    }


    def parse(self, response):
        ip_address = response.text.strip()  # Extract the IP address
        yield {"ip_address": ip_address}
