import scrapy
from scrapy import Selector
from spider2107.items import MovieItem
from scrapy.http import Request, Response

class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["https://movie.douban.com/top250"]

    def parse(self, response:Response):
        sel = Selector(response)
        list_items = sel.css('#content > div > div.article > ol > li')
        for list_item in list_items:
            movie_item = MovieItem()
            movie_item['title'] = list_item.css('span.title::text').extract_first()
            movie_item['rank'] = list_item.css('span.rating_num::text').extract_first()
            movie_item['subject'] = list_item.css('span.inq::text').extract_first()
            yield movie_item

        # hrefs_list = sel.css('#content > div > div.article > div.paginator > a::attr(href)')
        # for href in hrefs_list:
        #     url = response.urljoin(href.extract())
        #     yield Request(url=url)
        next_page_href = sel.css('#content > div > div.article > div.paginator > span.next > link::attr(href)')
        next_url = response.urljoin(next_page_href.extract_first())
        # print(next_url)
        yield Request(url=next_url)