# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NyaaItem(scrapy.Item):
    category = scrapy.Field()
    title = scrapy.Field()
    torrent = scrapy.Field()
    magnet = scrapy.Field()
    size = scrapy.Field()
    date = scrapy.Field()
    seeder = scrapy.Field()
    leecher = scrapy.Field()
    downloads = scrapy.Field()

class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    rank = scrapy.Field()
    subject = scrapy.Field()
    duration = scrapy.Field()
    intro = scrapy.Field()
