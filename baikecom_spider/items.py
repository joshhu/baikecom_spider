# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BaikecomSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    page_url = scrapy.Field()
    baike_id = scrapy.Field()
    title = scrapy.Field()
    name = scrapy.Field()
    text = scrapy.Field()

