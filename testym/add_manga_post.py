import requests
import post_login

url = 'http://127.0.0.1:8000/manga/show/'

path = '1520984778_site-portfolio_6.jpg'


with open(path, 'rb') as a, open(path,'rb') as f:
    date = {
        'title': 'myaso',
        'description': 'jhfklasd jfjdaslf ads',
        'year': '2001-02-25',
    }

    files = {'chapters': a, 'img': f}

    response = requests.post(url=url, data=date, headers=post_login.headers, files=files)

if response.status_code == 201:
    print('Успешно', response.text)
else:
    print('Ошибка', response.status_code, response.text)
