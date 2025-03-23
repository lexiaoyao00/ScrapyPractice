import scrapy
from scrapy import Request,Selector
from scrapy.http import Response
from scrapy_playwright.page import PageMethod

from urllib.parse import urlencode
import urllib.parse
import re

from mySpider.items import HanimeItem
import time

class HanimeSpider(scrapy.Spider):
    name = "hanime"
    allowed_domains = ["hanime1.me"]
    # start_urls = ["https://hanime1.me/"]

    max_pages = 3

    base_urls = {
        'origin':"https://hanime1.me/",
        'search':"https://hanime1.me/search",
        'watch':"https://hanime1.me/watch",
        'download':"https://hanime1.me/download"
    }

    custom_settings = {
        "PLAYWRIGHT_BROWSER_TYPE ":"chromium",
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "DOWNLOAD_HANDLERS": {
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "PLAYWRIGHT_LAUNCH_OPTIONS":{
            "headless": False,
            "slow_mo": 1000,  # 每个操作之间暂停 1000 毫秒
        },
        # "ITEM_PIPELINES": {"mySpider.pipelines.HanimePipeline": 300},
    }

    def __init__(self,*args, **kwargs):
        super(HanimeSpider,self).__init__(*args,**kwargs)
        self.page_count = 0

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

        url = f"{self.base_urls['search']}?{urlencode(params, doseq=True)}"
        headers = {
            "Referer":"https://hanime1.me/",
            "cookie":"remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6IlFkajlPZDEyQlFHYmdaWmtkMks4MVE9PSIsInZhbHVlIjoiNHhcLzZJQlVBRUtyMFFCaGhzNHk2REJQOW5rU2tRdGdrYzU1YVJwV2o0YmlxeisyS2RcL0RQOHZjanRoWlhIQUIwOGw4dFNONW9sK0xrRm1mUmp1RmFicWhLalhmUFpPbFFuKzFrMG00Zm1vUkwyMWtBUnBXT2djV0l4NlZMaWt2YWsyV005eEM3c21EaVwvVWl3SFErXC9PSnZ0TXZGRDBBQVo0WXFsMU4rcjI5aHlTbG5ZNFJ5R0tOT2tKTkNsdFVHXC8iLCJtYWMiOiIxNmYzODhmZDM0OGJiYzIzNzg5MDU4ZGRjZjQzNjJjYmYzMzk2MTkyODQwZjcxNzg0YWJjYjBiMzFjYWExYWNiIn0%3D; __atuvc=0%7C34%2C52%7C35%2C0%7C36%2C0%7C37%2C79%7C38; _gid=GA1.2.350206574.1739715472; cf_clearance=Qi3BYxmer6_1oL0GMzKKafNyFAECuWnyH8uqtkbg9NY-1739716877-1.2.1.1-m0mtan2_apCe.qVj_3vnX2nlg1qBK0rVj5TtwFhwRyr6VJQZDZBKwCjELZfX8e_y7jhyIR8NMTB4ZKi7pq.hEE6CEq5dps158FPCGW7WgkR_Mndc.2pXyGvTqCZXXNLd2nhlFz1qAPl.mw3ML.ZsotWoM0XOyv_bA9Cn4V3yy3gRR93lzBmH_ST8wb.T.WDs71_XcvJ2N8xIbqZ8KkNO5V.H6gpjSyxciFp7xK3vncBdvHddM_1AhwEZPOryU2ZdvJRbVI79URVFciKLG9jnwM5zAB5Hr58IucdI6oSeWV4; XSRF-TOKEN=eyJpdiI6IjFuM2c5Y2lYemtvK05iVXVhSEpoUVE9PSIsInZhbHVlIjoibHNwOGIxMnBxXC9xa1hvSmxKRklvZzB5cDJIS1FVSmZaUmdZSVpjRjhKZlM4b1BSQ1krZ0p5VkdIZFFla0ZWYksiLCJtYWMiOiJjYmM4MzM4MzBmZGI5OTQwMmFiZWM5NTk1NzQyYzE0ZDM4NmJlNDdkNDdlNzA3ZjBhZTNmNDEzZDIxNTNlZWQ5In0%3D; hanime1_session=eyJpdiI6IjQyb0FcL2hmMHVHczdreElvUlhzRUlBPT0iLCJ2YWx1ZSI6IjVGWnlsYVZBU3pSZU91bzkwaUhhcTJMK3d5cDVhOTlzdEVuWEFXbTB3dmdrOWhpRFd6MWR5TGtQR2VyQjJzQ20iLCJtYWMiOiIwM2VjYzkzZjBiZmQ5ODkxOTUxODM5NjMzMzYyMTY4ZmU5ZGRlNDgyODI5MzhjNTIxMTU5MTkyNWU3ZjU5NzczIn0%3D; _ga=GA1.1.1934604255.1705925664; _ga_2JNTSFQYRQ=GS1.1.1739715471.13.1.1739717281.0.0.0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",

            }

        yield Request(url=url,
                      meta=dict(
                        playwright=True,
                        playwright_include_page=True,
                        playwright_page_methods=[
                            PageMethod('wait_for_selector', 'div#home-rows-wrapper'),
                        ]
                    ))

    async def parse(self, response:Response):
        page = response.meta['playwright_page']
        # title = await page.title()

        content = await page.content()
        sel = Selector(text=content)

        item_feild = sel.css('div#home-rows-wrapper')
        hanime = HanimeItem()
        # watch_hrefs = item_feild.css('div.home-rows-videos-wrapper a:not([target])::attr(href)')
        item_links = item_feild.css('div.home-rows-videos-wrapper a:not([target])')
        # href = item.css('a[target="_blank"]::attr(href)').extract_first()
        for link in item_links:
            href = link.attrib['href']
            print(f'================href:{href}')
            hanime['watch_href'] = href

            mobj = re.search(r'hanime.*?v=([\d]+)', href)
            id = mobj.group(1)
            print(f'================id:{id}')
            hanime['id'] = id

            title = link.css('div.home-rows-videos-title::text').extract_first()
            print(f'================title:{title}')
            hanime['title'] = title

            img_src = link.css('img::attr(src)').extract()
            print(f'================img_src:{img_src}')

            yield hanime

        # next_url = self.base_urls['search'] + sel.css('a[class="page-link"][rel="next"]::attr(href)').extract()
        next_url = self.base_urls['search'] + sel.css('a[class="page-link"][rel="next"]::attr(href)').extract_first()
        print(f'================next_url:{next_url}')


        self.page_count += 1
        # if self.page_count <= self.max_pages and next_url:

        #     yield Request(url=next_url,
        #                 meta=dict(
        #                     playwright=True,
        #                     playwright_include_page=True,
        #                     playwright_page_methods=[
        #                         PageMethod('wait_for_selector', 'div#home-rows-wrapper'),
        #                     ]
        #                 ),
        #                 callback=self.parse
        #                 )


        await page.close()


    async def parse_watch_page(self, response:Response):
        pass

