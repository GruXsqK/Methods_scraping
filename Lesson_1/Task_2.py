# Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.


import requests
import json


main_link = 'http://ws.audioscrobbler.com/2.0/?'

api_key = 'input_your_api_key'
user = 'input_user_name'

if api_key == 'input_your_api_key':
    with open(f'api_key.json', 'r') as f:
        api_key = json.load(f)

if user == 'input_user_name':
    with open(f'user.json', 'r') as f:
        user = json.load(f)


api_metods = {'get_artists': 'library.getartists',
              'user_info': 'User.getInfo',
              'user_loved_tracks': 'User.getLovedTracks',
              'user_top_album': 'User.getTopAlbums'
              }

activ_metod = api_metods['user_info']

params = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
          'api_key': api_key,
          'method': activ_metod,
          'user': user,
          'format': 'json'
          }

response = requests.get(f'{main_link}', params=params)

if response.ok:

    data = json.loads(response.text)

    with open(f'{activ_metod}.json', 'w') as f:
        json.dump(data, f, indent=2)

else:
    print(f'Ошибка {response.status_code}')
