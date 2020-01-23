# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


class JobparserHhItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    salary = scrapy.Field(input_processor=MapCompose())
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    valuta = scrapy.Field()
    source = scrapy.Field(output_processor=TakeFirst())


class JobparserSjItem(scrapy.Item):
    json_item = scrapy.Field(input_processor=MapCompose())
