import requests
import testim.Profile.post_login

url = 'http://127.0.0.1:8000/manga/show/'

date = {
    'title': 'myaso',
    'description': 'jhfklasd jfjdaslf ads',
    'year': '2001-02-25',
    "chapters": '1520984778_site-portfolio_6_vtRuAil.jpg',
    'img': '1520984778_site-portfolio_6_vtRuAil.jpg'
}

response = requests.post(url=url, json=date, headers=testim.Profile.post_login.headers)

if response.status_code == 201:
    print('Успешно', response.text)
else:
    print('Ошибка', response.status_code, response.text)