import requests
import post_login

url = 'http://127.0.0.1:8000/reviews/comments/'
data = {
    "message": "Это еще один комментарий2131221",
    "manga": '1'
}
response = requests.post(url=url, json=data, headers=post_login.headers)


if response.status_code == 201:
    print('Записи(-ь) добавлены(-а): ', response.text)
else:
    print('Ошибка', response.status_code, response.text)
