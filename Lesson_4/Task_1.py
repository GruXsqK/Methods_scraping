# 1)Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex.news
# Для парсинга использовать xpath. Структура данных должна содержать:
# * название источника,
# * наименование новости,
# * ссылку на новость,
# * дата публикации
# 2)Сложить все новости в БД


import requests
import pymongo
from lxml import html


def news_from_mail():

    all_news_mail = []

    main_link_mail = "https://mail.ru/"
    response = requests.get(main_link_mail,
                            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; '
                                                   'Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                                   'Chrome/78.0.3904.108 Safari/537.36'}
                            )

    root = html.fromstring(response.text)

    if response.ok:

        news_lst_mail = root.xpath("//div[@class='highlighter']//following-sibling::a[last()]")

        for itm in news_lst_mail:
            news = itm.xpath(".//text()")[0].replace('\xa0', ' ')
            link = itm.xpath(".//@href")[0]

            root_news = html.fromstring(requests.get(link).text)

            source = root_news.xpath("//a[@class='link color_gray breadcrumbs__link']/@href")[0]
            date = root_news.xpath("//span[@datetime]/@datetime")[0]

            news_mail = {'Источник': source,
                         'Новость': news,
                         '_id': link,
                         'Дата': date}

            all_news_mail.append(news_mail)

        return all_news_mail

    else:
        return False


def news_from_lent():

    all_news_lent = []

    main_link_lent = "https://lenta.ru/"
    response = requests.get(main_link_lent,
                            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; '
                                                   'Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                                   'Chrome/78.0.3904.108 Safari/537.36'}
                            )

    root = html.fromstring(response.text)

    if response.ok:

        news_lst_lent = root.xpath("//section[contains(@class, 'b-top7-for-main')]/div/div"
                                   "[not(contains(@class, 'button-more-news'))]")

        for itm in news_lst_lent:

            link_root = itm.xpath(".//a/@href")[0]

            if link_root[:4] == 'http':

                link = link_root
                source = 'http://' + link_root.split('//')[1].split('/')[0] + '/'

            else:

                source = main_link_lent
                link = main_link_lent[:-1] + itm.xpath(".//a/@href")[0]

            news_lent = {'Источник': source,
                         'Новость': itm.xpath(".//a/text()")[0].replace('\xa0', ' '),
                         '_id': link,
                         'Дата': itm.xpath(".//a/time/@datetime")[0]}

            all_news_lent.append(news_lent)

        return all_news_lent

    else:
        return False


def news_from_ydx():

    all_news_ydx = []

    main_link_ydx = "https://yandex.ru/news"
    response = requests.get(main_link_ydx,
                            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; '
                                                   'Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                                   'Chrome/78.0.3904.108 Safari/537.36'}
                            )

    root = html.fromstring(response.text)

    if response.ok:

        news_lst_ydx = root.xpath("//h2")

        for itm in news_lst_ydx:

            root_link = itm.xpath("../../div[@class='story__info']/div[@class='story__date']/text()")[0]

            news_ydx = {'Источник': root_link[:-6].replace(' вчера\xa0в', ''),
                        'Новость': itm.xpath(".//a/text()")[0].replace('\xa0', ' '),
                        '_id': "https://yandex.ru" + itm.xpath(".//@href")[0],
                        'Дата': root_link[-5:]}

            all_news_ydx.append(news_ydx)

        return all_news_ydx

    else:
        return False


try:
    mail_collect = pymongo.MongoClient('localhost', 27017)['news']['mail']
    mail_collect.insert_many(news_from_mail(), ordered=False)

except pymongo.errors.BulkWriteError:
    pass

try:
    lent_collect = pymongo.MongoClient('localhost', 27017)['news']['lent']
    lent_collect.insert_many(news_from_lent(), ordered=False)

except pymongo.errors.BulkWriteError:
    pass

try:
    ydx_collect = pymongo.MongoClient('localhost', 27017)['news']['ydx']
    ydx_collect.insert_many(news_from_ydx(), ordered=False)

except pymongo.errors.BulkWriteError:
    pass
