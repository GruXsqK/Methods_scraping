# 1) Необходимо собрать информацию о вакансиях на вводимую должность (используем input или
# через аргументы) с сайта superjob.ru и hh.ru. Приложение должно анализировать несколько страниц
# сайта(также вводим через input или аргументы). Получившийся список должен содержать в себе
# минимум:
# *Наименование вакансии
# *Предлагаемую зарплату (отдельно мин. и и отдельно макс.)
# *Ссылку на саму вакансию
# *Сайт откуда собрана вакансия
# По своему желанию можно добавить еще работодателя и расположение. Данная структура должна
# быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью
# dataFrame через pandas.


import requests
import time
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs


main_link_hh = 'https://spb.hh.ru'
main_link_sj = 'https://www.superjob.ru'


def dict_vacancy():
    return {'Вакансия': None,
            'Зарплата мин.': None,
            'Зарплата мкс.': None,
            'Валюта': None,
            'Ссылка': None,
            'Сайт': None}


def salary_tpl(salary_str, dlm='—', spl='\xa0'):

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

    if not(salary_str.startswith('По')) and salary_str:

        valuta = val_symbol(salary_str.split(spl)[-1])
        len_str = len(salary_str.split(spl)[-1])

        if salary_str[:2].isdigit():

            spam = salary_str[:-len_str].replace(' ', '').replace('\xa0', '').split(dlm)
            min_salary = int(spam[0])
            max_salary = int(spam[1])

        elif salary_str[:2] == 'от':

            min_salary = int(salary_str.replace(' ', '').replace('\xa0', '')[2:-len_str])

        elif salary_str[:2] == 'до':

            max_salary = int(salary_str.replace(' ', '').replace('\xa0', '')[2:-len_str])

    return min_salary, max_salary, valuta


vacancy_search = input('Введите вакансию\n')
page_sj = 1

vacancy_lst = []


while True:

    response_sj = requests.get(f'{main_link_sj}/vacancy/search/?keywords={vacancy_search}'
                               f'&geo%5Bc%5D%5B0%5D=1&page={page_sj}')

    if response_sj.ok:

        html_parsed_sj = bs(response_sj.text, 'lxml')
        vacancy_on_page_sj = html_parsed_sj.findAll('a', {'class': '_3dPok'} and {'class': '_1QIBo'})

        for vac in vacancy_on_page_sj:

            vacancy = dict_vacancy()

            vacancy['Вакансия'] = vac.getText()
            vacancy['Ссылка'] = main_link_sj + vac['href']
            vacancy['Сайт'] = main_link_sj

            salary = vac.findParent().findParent().find('span', {'class': 'f-test-text-company-item-salary'}).getText()

            vacancy['Зарплата мин.'], vacancy['Зарплата мкс.'], vacancy['Валюта'] = salary_tpl(salary)

            vacancy_lst.append(vacancy)

        if html_parsed_sj.find('a', {'class': 'f-test-button-dalshe'}):
            page_sj += 1
        else:
            break

    else:
        print(f'Ошибка {response_sj.status_code}')
        break


page_hh = 0

while True:

    response_hh = requests.get(f'{main_link_hh}/search/vacancy?L_is_autosearch=false&area=113&'
                               f'clusters=true&enable_snippets=true&text={vacancy_search}&page={page_hh}',
                               headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; '
                                                      'Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                                      'Chrome/78.0.3904.108 Safari/537.36'})

    if response_hh.ok:

        html_parsed_hh = bs(response_hh.text, 'lxml')
        vacancy_on_page_hh = html_parsed_hh.findAll('a', {'data-qa': 'vacancy-serp__vacancy-title'})

        for vac in vacancy_on_page_hh:

            vacancy = dict_vacancy()

            vacancy['Вакансия'] = vac.getText()
            vacancy['Ссылка'] = vac['href']
            vacancy['Сайт'] = main_link_hh

            compensation = vac.findParent().findParent().findParent().findParent()\
                .find('div', {'data-qa': 'vacancy-serp__vacancy-compensation'})

            if compensation:

                salary = compensation.getText()

                vacancy['Зарплата мин.'], vacancy['Зарплата мкс.'], vacancy['Валюта'] = \
                    salary_tpl(salary, dlm='-', spl=' ')

            vacancy_lst.append(vacancy)

        if html_parsed_hh.find('a', {'data-qa': 'pager-next'}).getText() == 'дальше':
            page_hh += 1
            time.sleep(np.random.sample()*3)
        else:
            break

    else:
        print(f'Ошибка {response_hh.status_code}')
        break

df = pd.DataFrame(vacancy_lst)
