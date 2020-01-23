# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from jobparser.items import JobparserHhItem


class HhSpider(scrapy.Spider):
    name = 'hh'
    allowed_domains = ['hh.ru']
    start_urls = [f'https://spb.hh.ru']

    def __init__(self, vacancy_search):
        super(HhSpider, self).__init__()
        self.start_urls = [f'https://spb.hh.ru/search/vacancy?area=&st=searchVacancy&text={vacancy_search}']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy_lst = response.css('div.vacancy-serp '
                                   'div.vacancy-serp-item '
                                   'div.vacancy-serp-item__row_header '
                                   'a.bloko-link::attr(href)').extract()

        for link in vacancy_lst:
            yield response.follow(link, callback=self.vacancy_parse)

    @staticmethod
    def vacancy_parse(response: HtmlResponse):
        loader = ItemLoader(item=JobparserHhItem(), response=response)
        loader.add_xpath('name', '//h1[@class=\'header\']//span/text()')
        loader.add_css('salary', 'div.vacancy-title p.vacancy-salary::text')
        loader.add_value('_id', response.url)
        loader.add_value('source', HhSpider.allowed_domains)
        yield loader.load_item()
