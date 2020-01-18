# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjSpider(scrapy.Spider):
    name = 'sj'
    vacancy_search = 'python'
    allowed_domains = ['superjob.ru']
    start_urls = [f'https://www.superjob.ru/vacancy/search/?keywords={vacancy_search}&geo%5Bc%5D%5B0%5D=1']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.f-test-link-Dalshe::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy_lst = response.css('a._1QIBo::attr(href)').extract()

        for link in vacancy_lst:
            yield response.follow(link, callback=self.vacancy_parse)

    @staticmethod
    def vacancy_parse(response: HtmlResponse):
        name = response.css('h1::text').extract_first()
        salary = response.xpath('//span[@class=\'_3mfro _2Wp8I ZON4b PlM3e _2JVkc\']'
                                '/descendant-or-self::span/text()').extract()
        yield JobparserItem(_id=response.url, name=name, salary=salary, source=SjSpider.allowed_domains[0])
