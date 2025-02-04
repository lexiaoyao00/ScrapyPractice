import scrapy


class HanimeSpider(scrapy.Spider):
    name = "hanime"
    allowed_domains = ["hanime1.me"]
    start_urls = ["https://hanime1.me/"]

    def parse(self, response):
        pass
