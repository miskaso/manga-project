import requests
import profile_login
# Добавить автора


url = 'http://127.0.0.1:8000//manga/authors/'

path = '1520984778_site-portfolio_6.jpg'

with open(path, 'rb') as a, open(path,'rb') as f:
    data = {
        'name': 'Александр',
        'lastname': 'Инкогнито',
        'bio': 'блаблабла',
    }

    files = {'chapters': a, 'img': f}

    response = requests.post(url=url, data=data, headers=profile_login.headers,
                             files=files)


if response.status_code == 201:
    print('Автор создан. ', response.text)
else:
    print('Ошибка ', response.status_code, response.text)

