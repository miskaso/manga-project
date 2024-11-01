import requests
import post_login

url = 'http://127.0.0.1:8000/fav_recom/favorite/'

response = requests.get(url=url, headers=post_login.headers)

if response.status_code == 200:
    print('Записи(-ь) получены(-а): ', response.text)
else:
    print('Ошибка', response.status_code, response.text)
