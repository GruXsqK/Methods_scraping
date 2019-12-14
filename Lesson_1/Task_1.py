# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.


import requests
import json


main_link = 'https://api.github.com'
user_name = 'gruxsqk'

response = requests.get(f'{main_link}/users/{user_name}/repos')

if response.ok:

    data = [itm['name'] for itm in json.loads(response.text)]

    with open(f'{user_name}.json', 'w') as f:
        json.dump(data, f, indent=2)

else:
    print('Неверное имя пользователя')
