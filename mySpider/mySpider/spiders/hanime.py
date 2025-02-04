import scrapy
from scrapy import Request,Selector
from scrapy.http import Response

from urllib.parse import urlencode
import urllib.parse

from mySpider.items import MyspiderItem

class HanimeSpider(scrapy.Spider):
    name = "hanime"
    allowed_domains = ["hanime1.me"]
    # start_urls = ["https://hanime1.me/"]

    def start_requests(self):
        query = self.settings.get('query', '')
        type = self.settings.get('type', '')
        genre = self.settings.get('genre', '')
        tags = self.settings.get('tags[]', [])
        sort = self.settings.get('sort', '')
        year = self.settings.get('year', '')
        month = self.settings.get('month', '')

        params = {
            'query': query,
            'type': type,
            'genre': genre,
            'tags[]': tags,
            'sort': sort,
            'year': year,
            'month': month,

        }
        # encoded_params = "&".join(f"{urllib.parse.quote_plus(k)}={urllib.parse.quote_plus(str(v))}"
        #                           if isinstance(v, str) else f"{urllib.parse.quote_plus(k)}={urllib.parse.quote_plus(','.join(map(str, v)))}"
        #                           for k, v in params.items())

        url = f"https://hanime1.me/search?{urlencode(params, doseq=True)}"
        yield Request(url=url)

    def parse(self, response:Response):
        sel = Selector(response)
        list_items = sel.css('div.home-rows-videos-wrapper')
        for item in list_items:
            hanime = MyspiderItem()
            href = item.css('a:not([target="_blank"])::attr(href)')
            print(href)

            yield hanime
