import requests
import post_login

url = 'http://127.0.0.1:8000/reviews/review/'
data = {
    "manga": 1,
    "rating": '5',
    "message": "Отличная манга, мне понравилась!"
}
response = requests.post(url=url, json=data, headers=post_login.headers)

print(post_login.headers)
if response.status_code == 201:
    print('Записи(-ь) добавлены(-а): ', response.text)
else:
    print('Ошибка', response.status_code, response.text)
