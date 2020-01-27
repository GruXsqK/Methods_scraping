# Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
# Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient, errors
import hashlib
import json
import time


start_link = 'https://www.mvideo.ru'
item = {}

client = MongoClient('localhost', 27017)
collection = client.mvideo.hits

chrome_options = Options()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1920, 1080)
driver.get(start_link)
assert 'М.Видео' in driver.title

driver.execute_script("arguments[0].click();", driver
                      .find_elements_by_css_selector('div.sel-hits-block')[0]
                      .find_elements_by_css_selector('div.carousel-paging > a')[-1])

time.sleep(3)

hits_on_page = driver.find_elements_by_css_selector("ul.accessories-product-list")[1]\
    .find_elements_by_css_selector("li")

for itm in hits_on_page:
    tag = itm.find_element_by_tag_name('a')
    item['link'] = tag.get_attribute('href')
    data = json.loads(tag.get_attribute('data-product-info'))
    item['name'] = data['productName']
    item['price'] = data['productPriceLocal']
    item['_id'] = hashlib.sha1(bytes(item['name'], encoding='utf-8')).hexdigest()

    try:
        collection.insert_one(item)
    except errors.PyMongoError:
        pass

driver.quit()
