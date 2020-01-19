# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from jobparser.items import JobparserSjItem


class SjSpider(scrapy.Spider):
    name = 'sj'
    allowed_domains = ['superjob.ru']
    start_urls = [f'https://www.superjob.ru']

    def __init__(self, vacancy_search):
        super(SjSpider, self).__init__()
        self.start_urls = [f'https://www.superjob.ru/vacancy/search/?keywords={vacancy_search}&geo%5Bc%5D%5B0%5D=1']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.f-test-link-Dalshe::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy_lst = response.css('a._1QIBo::attr(href)').extract()

        for link in vacancy_lst:
            yield response.follow(link, callback=self.vacancy_parse)

    @staticmethod
    def vacancy_parse(response: HtmlResponse):
        loader = ItemLoader(item=JobparserSjItem(), response=response)
        loader.add_xpath('json_item', '//script[@type=\'application/ld+json\']/text()')
        yield loader.load_item()
