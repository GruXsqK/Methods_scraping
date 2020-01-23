# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import json


class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]

        if spider.name == 'hh':
            item['min_salary'], item['max_salary'], item['valuta'] = \
                JobparserPipeline.salary_editor(item['salary'])
            del(item['salary'])

            if item['name']:
                collection.insert_one(item)

        elif spider.name == 'sj':
            item_db = {}
            data = json.loads(item['json_item'][-1])
            item_db['_id'] = data.get('url')
            item_db['name'] = data.get('title')
            item_db['source'] = spider.allowed_domains[0]

            item_db['valuta'] = None
            item_db['min_salary'] = None
            item_db['max_salary'] = None

            salary = data.get('baseSalary')

            if salary:
                item_db['valuta'] = salary.get('currency')
                value = salary.get('value')

                if value:
                    item_db['min_salary'] = value.get('minValue')
                    item_db['max_salary'] = value.get('maxValue')

            collection.insert_one(item_db)

        return item

    @staticmethod
    def salary_editor(salary_lst):

        min_salary = None
        max_salary = None
        valuta = None

        def val_symbol(a):
            val_dct = {'₽': 'RUB',
                       'USD': 'USD',
                       'руб.': 'RUB',
                       'бел.\xa0руб.': 'BYN',
                       'KZT': 'KZT',
                       'RUB': 'RUB',
                       'EUR': 'EUR',
                       'грн.': 'UAH'}
            return val_dct[a]

        if salary_lst[0].replace(' ', '') == 'до':
            max_salary = int(salary_lst[1].replace('\xa0', ''))
            valuta = val_symbol(salary_lst[3])

        elif salary_lst[0].replace(' ', '') == 'от':
            min_salary = int(salary_lst[1].replace('\xa0', ''))

            if salary_lst[2].replace(' ', '') == 'до':
                max_salary = int(salary_lst[3].replace('\xa0', ''))
                valuta = val_symbol(salary_lst[5])

            else:
                valuta = val_symbol(salary_lst[3])

        return min_salary, max_salary, valuta
