import requests
import post_login

url = 'http://127.0.0.1:8000/profile/prof/'
response = requests.get(url=url, headers=post_login.headers)

if response.status_code == 200:
    print('Успешно!', response.json())
else:
    print('Ошибка', response.status_code, response.text)