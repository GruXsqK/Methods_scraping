# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from youlaparser.items import YoulaparserItem
from scrapy.loader import ItemLoader


class YoulaSpider(scrapy.Spider):
    name = 'youla'
    allowed_domains = ['youla.ru']
    start_urls = ['https://youla.ru']

    def __init__(self, category):
        super(YoulaSpider, self).__init__()
        self.start_urls = [f'https://youla.ru/all/{category}']

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath("//li[@class='product_item']/a/@href").extract()
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=YoulaparserItem(), response=response)
        loader.add_value('_id', response.url)
        loader.add_css('name', "h1::text")
        loader.add_xpath('price', '//span[@class=\'sc-eNPDpu draEbH\']/text()')
        loader.add_xpath('photos', '//div[@class=\'sc-hUfwpO sc-imABML fEIkBF\']')
        loader.add_xpath('attr', '//li[@data-test-block="Attributes"]')
        yield loader.load_item()
