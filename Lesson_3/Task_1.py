# 1) Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# записывающую собранные вакансии в созданную БД
# 2) Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой
# больше введенной суммы
# 3)*Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.
# Доработать функцию, которая будет обновлять старые вакансии.


from pymongo import MongoClient
import Scraper as Sc


def add_new_vacancy(vacancy_for_db, site):

    collect = MongoClient('localhost', 27017)[vacancy_for_db][site]
    lst_vacancy = []

    if site == 'hh':

        lst_vacancy = Sc.parse_hh(vacancy_for_db)[0]

    elif site == 'sj':

        lst_vacancy = Sc.parse_sj(vacancy_for_db)[0]

    for itm in lst_vacancy:

        itm['_id'] = itm.pop('Ссылка')

        if not any([itm for itm in collect.find({'_id': itm['_id']})]):

            collect.insert_one(itm)

        elif itm not in ([itm for itm in collect.find({'_id': itm['_id']})]):

            collect.update_one({'_id': itm['_id']},
                               {'$set': {'Зарплата мин': itm['Зарплата мин'],
                                         'Зарплата мкс': itm['Зарплата мкс'],
                                         'Валюта': itm['Валюта']}})

    return True


def get_items_db(db_vacancy, site, n):

    return MongoClient('localhost', 27017)[db_vacancy][site].find().limit(n)


def search_vacancy_salary(db_vacancy, site, salary, sig='='):

    sigils = {'>': '$gt',
              '<': '$lt',
              '=': '$eq',
              '>=': '$gte',
              '<=': '$lte'}

    return MongoClient('localhost', 27017)[db_vacancy][site].find({'$or': [
        {'Зарплата мин': {sigils[sig]: salary}}, {'Зарплата мкс': {sigils[sig]: salary}}]})


if __name__ == "__main__":

    vacancy_for_add_db = 'java'

    print('Вакансии из sj добавлены' if add_new_vacancy(vacancy_for_add_db, 'sj') else 'Ошибка добавления из sj')
    print('Вакансии из hh добавлены' if add_new_vacancy(vacancy_for_add_db, 'hh') else 'Ошибка добавления из hh')

    print('Первые 10 вакансий в коллекции sj:\n', *get_items_db(vacancy_for_add_db, 'sj', 10))
    print('Вакансии из sj с зарплатой выше 150000:\n', *search_vacancy_salary(vacancy_for_add_db, 'sj', 150000, '>'))
