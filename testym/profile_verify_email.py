import requests
import profile_login

url = '/api/auth/registration/verify-email/'

key = '123564'
data = {
    'key': key
}

response = requests.post(url=url, data=data, headers=profile_login.headers)

if response.status_code == 201:
    print('Запрос выполнен.', response.text)
else:
    print('Ошибка', response.text, response.status_code)
