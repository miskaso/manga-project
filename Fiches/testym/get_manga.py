import requests
import profile_login

url = 'http://127.0.0.1:8000/manga/show/'

response = requests.get(url=url, headers=post_login.headers)

if response.status_code == 200:
    print('Записи(-ь) получены(-а): ', response.text)
else:
    print('Ошибка', response.status_code, response.text)


# Есть поддержка сложных фильтраций
url = 'http://127.0.0.1:8000/manga/show/?author=Ктото&category=Комедия'

response = requests.get(url=url, headers=post_login.headers)

if response.status_code == 200:
    print('Записи(-ь) сложной фильтрации получены(-а): ', response.text)
else:
    print('Ошибка', response.status_code, response.text)


# Для сортировки по топу отправить пустой top
url = 'http://127.0.0.1:8000/manga/show/?top'

response = requests.get(url=url, headers=post_login.headers)

if response.status_code == 200:
    print('Записи(-ь) из топа получены(-а): ', response.text)
else:
    print('Ошибка', response.status_code, response.text)


# Для сортировки по новизне отправить new=1
url = 'http://127.0.0.1:8000/manga/show/?new=1'

response = requests.get(url=url, headers=post_login.headers)

if response.status_code == 200:
    print('Записи(-ь) по новизне получены(-а): ', response.text)
else:
    print('Ошибка', response.status_code, response.text)