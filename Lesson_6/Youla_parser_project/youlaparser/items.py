# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


class YoulaparserItem(scrapy.Item):
    # # define the fields for your item here like:
    _id = scrapy.Field(output_processor=TakeFirst())
    data = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field()
    price = scrapy.Field()
    photos = scrapy.Field()
    params = scrapy.Field()
