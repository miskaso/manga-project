import requests

url = "http://127.0.0.1:8000/api/auth/registration/"

data = {
    "username": "ty342da",
    "password1": "t2yweda14sS",
    "password2": "t2yweda14sS"
}
response = requests.post(url, json=data)
if response.status_code == 201:
    access = response.json().get('access')
    headers = {
        "Authorization": f"Bearer {access}"
    }
    print('Логин успешен.')
else:
    print('Ошибка при отправке запроса:', response.status_code, response.text)

