import requests
import post_login


url = "http://127.0.0.1:8000/profile/prof/"

data = {
    "bio": "asdfasdfdsafsadfsfasdfsdafdsaasd",
    'telephone': '+996995803103',
    'year': '2001'
}
response = requests.post(url=url, json=data, headers=post_login.headers)

if response.status_code == 201:
    access = response.json().get('access')

    print('Профиль создан.')
else:
    print('Ошибка при отправке запроса:', response.status_code, response.text)


