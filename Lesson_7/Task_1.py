# Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о
# письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from pymongo import MongoClient, errors
from selenium.common.exceptions import *
import hashlib


login = 'study.ai_172'
domain = 'mail.ru'
password = 'NewPassword172'
start_link = 'https://m.mail.ru/login'

client = MongoClient('localhost', 27017)
collection = client.emails[login]

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)

driver.get(start_link)
assert 'Вход — Почта Mail.Ru' in driver.title

elem = driver.find_element_by_name('Login')
elem.send_keys(login)

elem = driver.find_element_by_name('Domain')
select = Select(elem)
select.select_by_visible_text(domain)

elem = driver.find_element_by_name('Password')
elem.send_keys(password)
elem.submit()
assert 'Входящие' in driver.title

try:
    letter_link = driver.find_element_by_xpath("//a[@class='messageline__link']").get_attribute('href')

    while True:
        item = {}
        driver.get(letter_link)

        sender = driver.find_element_by_tag_name('strong').text.split('<')

        item['sender_name'] = sender[0]
        item['sender_email'] = sender[1][:-1]
        item['date'] = driver.find_element_by_class_name('readmsg__mail-date').text
        item['theme'] = driver.find_element_by_class_name('readmsg__theme').text
        item['text'] = driver.find_element_by_xpath("//*[@id='readmsg__body']").text
        item['_id'] = hashlib.sha1(bytes(item['date'] + item['theme'] + item['text'], encoding='utf-8')).hexdigest()

        try:
            collection.insert_one(item)
        except errors.PyMongoError:
            pass

        next_btn = driver.find_elements_by_xpath("//a[@class='readmsg__text-link']")[-1]

        if next_btn.text == 'Следующее':
            letter_link = next_btn.get_attribute('href')
        else:
            print("Конец")
            break

except NoSuchElementException:
    print("Писем нет")

driver.quit()
