# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhSpider(scrapy.Spider):
    name = 'hh'
    vacancy_search = 'python'
    allowed_domains = ['hh.ru']
    start_urls = [f'https://spb.hh.ru/search/vacancy?area=&st=searchVacancy&text={vacancy_search}']

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
        name = response.xpath('//h1[@class=\'header\']//span/text()').extract_first()
        salary = response.css('div.vacancy-title p.vacancy-salary::text').extract()
        yield JobparserItem(_id=response.url, name=name, salary=salary, source=HhSpider.allowed_domains[0])
