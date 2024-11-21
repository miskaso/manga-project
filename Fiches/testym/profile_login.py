import requests

# Вход в аккаунт

url = "http://127.0.0.1:8000/profile/api/token/"

data = {
    "username": "owner",
    "password": "t2yweda14sSa32"
}
response = requests.post(url, json=data)
if response.status_code == 200:
    access = response.json().get('access')
    headers = {
        "Authorization": f"Bearer {access}"
    }
    print('Логин успешен.')
else:
    print('Ошибка при отправке запроса:', response.status_code, response.text)

