import scrapy
from scrapy import Selector
from spider2107.items import MovieItem
from scrapy.http import Request, Response

class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["https://movie.douban.com/top250"]
    custom_settings = {
        "ITEM_PIPELINES": {"spider2107.pipelines.DoubanPipeline": 300},
    }

    def parse(self, response:Response,**kwargs):
        sel = Selector(response)
        list_items = sel.css('#content > div > div.article > ol > li')
        for list_item in list_items:
            detail_url = list_item.css('div.info > div.hd > a::attr(href)').extract_first()
            movie_item = MovieItem()
            movie_item['title'] = list_item.css('span.title::text').extract_first()
            movie_item['rank'] = list_item.css('span.rating_num::text').extract_first()
            movie_item['subject'] = list_item.css('span.inq::text').extract_first()
            yield Request(url=detail_url,
                          callback=self.parse_detail,
                          cb_kwargs={'item':movie_item}
                          )

        # next_page_href = sel.css('#content > div > div.article > div.paginator > span.next > link::attr(href)')
        # next_url = response.urljoin(next_page_href.extract_first())
        # yield Request(url=next_url)

    def parse_detail(self,response:Response,**kwargs):
        movie_item = kwargs['item']
        sel = Selector(response)
        movie_item['duration'] = sel.css('span[property="v:runtime"]::text').extract_first()
        movie_item['intro'] = sel.css('span[property="v:summary"]::text').extract_first()

        yield movie_item