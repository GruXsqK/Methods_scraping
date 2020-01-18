# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        item['min_salary'], item['max_salary'], item['valuta'] = \
            JobparserPipeline.salary_editor(item['salary'], spider.name)
        del(item['salary'])
        if item['name']:
            collection.insert_one(item)
        return item

    @staticmethod
    def salary_editor(salary_lst, site):

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

        def salary_hh(sal_lst):

            nonlocal min_salary, max_salary, valuta

            if sal_lst[0].replace(' ', '') == 'до':
                max_salary = int(sal_lst[1].replace('\xa0', ''))
                valuta = val_symbol(sal_lst[3])

            elif sal_lst[0].replace(' ', '') == 'от':
                min_salary = int(sal_lst[1].replace('\xa0', ''))

                if sal_lst[2].replace(' ', '') == 'до':
                    max_salary = int(sal_lst[3].replace('\xa0', ''))
                    valuta = val_symbol(sal_lst[5])

                else:
                    valuta = val_symbol(sal_lst[3])

            return min_salary, max_salary, valuta

        def salary_sj(sal_lst):

            nonlocal min_salary, max_salary, valuta

            if sal_lst[0].replace('\xa0', '').isdigit():
                if len(sal_lst) > 3:
                    min_salary = int(sal_lst[0].replace('\xa0', ''))
                    max_salary = int(sal_lst[4].replace('\xa0', ''))
                    valuta = val_symbol(sal_lst[6])
                else:
                    min_salary, max_salary = int(sal_lst[0].replace('\xa0', ''))
                    valuta = val_symbol(sal_lst[2])

            elif sal_lst[0].replace(' ', '') == 'от':
                min_salary = int(sal_lst[2].replace('\xa0', ''))
                valuta = val_symbol(sal_lst[4])

            elif sal_lst[0].replace(' ', '') == 'до':
                max_salary = int(sal_lst[2].replace('\xa0', ''))
                valuta = val_symbol(sal_lst[4])

            return min_salary, max_salary, valuta

        if site == 'hh':
            return salary_hh(salary_lst)
        elif site == 'sj':
            return salary_sj(salary_lst)
