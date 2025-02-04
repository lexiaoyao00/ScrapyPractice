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

            nyaa_item['category'] = item.css('td:nth-child(1) > a::attr(title)').extract_first()

            nyaa_item['title'] = item.css('td[colspan="2"] a::text').extract_first()

            nyaa_item['torrent'] = 'https://sukebei.nyaa.si' + item.css('td:nth-child(3) > a > i.fa-download').xpath('../@href').extract_first()
            nyaa_item['magnet'] = item.css('td:nth-child(3) > a > i.fa-magnet').xpath('../@href').extract_first()

            nyaa_item['size'] = item.css('td:nth-child(4)::text').extract_first()

            nyaa_item['date'] = item.css('td:nth-child(5)::text').extract_first()

            nyaa_item['seeder'] = item.css('td:nth-child(6)::text').extract_first()

            nyaa_item['leecher'] = item.css('td:nth-child(7)::text').extract_first()

            nyaa_item['downloads'] = item.css('td:nth-child(8)::text').extract_first()

            yield nyaa_item
