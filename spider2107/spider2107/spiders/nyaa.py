import scrapy
from scrapy import Selector
from spider2107.items import NyaaItem
from scrapy.http import Request, Response

class NyaaSpider(scrapy.Spider):
    name = "nyaa"
    allowed_domains = ["sukebei.nyaa.si"]
    # start_urls = ["https://sukebei.nyaa.si/"]
    custom_settings = {
        "ITEM_PIPELINES": {"spider2107.pipelines.NyaaPipeline": 300},
    }

    def start_requests(self):
        f = self.settings.get('f', '0')
        c = self.settings.get('c', '0_0')
        q = self.settings.get('q', 'MIDE-565')
        p = self.settings.get('p', '1')
        s = self.settings.get('s', 'id')
        o = self.settings.get('o', 'desc')
        url = f"https://sukebei.nyaa.si/?f={f}&c={c}&q={q}&p={p}&s={s}&o={o}"
        yield Request(url=url)

    def parse(self, response):
        sel = Selector(response)
        list_items = sel.css('body > div.container > div.table-responsive > table > tbody > tr')
        for item in list_items:
            nyaa_item = NyaaItem()
            nyaa_item['title'] = item.css('td[colspan="2"] a::text').extract_first()
            yield nyaa_item
