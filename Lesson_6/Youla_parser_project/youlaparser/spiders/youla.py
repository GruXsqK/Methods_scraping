# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from youlaparser.items import YoulaparserItem


class YoulaSpider(scrapy.Spider):
    name = 'youla'
    allowed_domains = ['youla.ru']
    start_urls = [f'https://youla.ru']

    def __init__(self, category):
        super(YoulaSpider, self).__init__()
        self.start_urls = [f'https://youla.ru/all/{category}']

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath("//li[@class='product_item']/a/@href").extract()
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)

    @staticmethod
    def parse_ads(response: HtmlResponse):
        loader = ItemLoader(item=YoulaparserItem(), response=response)
        loader.add_value('_id', response.url)
        loader.add_css('data', 'script::text')
        yield loader.load_item()
