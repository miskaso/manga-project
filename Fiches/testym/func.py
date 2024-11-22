import requests
import logging

logging.basicConfig(level=logging.INFO)


class BuildApi:
    base_url = 'http://127.0.0.1:8000'

    def __init__(self, url='/profile/api/token/', login='admi', password='admi'):
        """
        Инициализация API с авторизацией.
        """
        full_url = self._build_url(url)
        payload = {"username": login, "password": password}

        response = self._request("post", full_url, json=payload)
        if response and response.status_code == 200:
            access = response.json().get('access')
            if not access:
                raise ValueError("Токен доступа отсутствует в ответе сервера")
            self.headers = {"Authorization": f"Bearer {access}"}
            logging.info('Логин успешен.')
        else:
            raise ConnectionError(f"Ошибка авторизации: {response.status_code}, {response.text if response else ''}")

    def _build_url(self, url):
        """
        Построение полного URL.
        """
        return self.base_url + url

    def _request(self, method, url, **kwargs):
        """
        Обертка для выполнения HTTP-запросов.
        """
        try:
            response = requests.request(method, url, **kwargs)
            return response
        except requests.RequestException as e:
            logging.error(f"Ошибка при запросе {method.upper()} {url}: {str(e)}")
            return None

    def _process_response(self, result, success_message="Успех"):
        """
        Обрабатывает результат запроса и выводит сообщение.
        """
        if result['success']:
            print(success_message)
            if 'data' in result:
                print("Сообщение от сервера:", result[
                    'message'])
        else:
            print('Ошибка:', result.get('error', 'Неизвестная ошибка'), result[
                    'message'])

    def api_get(self, url):
        """
        Выполнение GET-запроса с автоматической обработкой результата.
        """
        full_url = self._build_url(url)
        response = self._request("get", full_url, headers=self.headers)

        result = {
            'success': response and response.status_code == 200,
            'data': response.json() if response and response.status_code ==
                                       200 else response.text,
            'status_code': response.status_code if response else None,
            'error': response.text if response and response.status_code !=
                                      200 else response.text,
            'message': response.text
        }
        self._process_response(result, "Данные успешно получены.")
        return result

    def api_post(self, data, url):
        """
        Выполнение POST-запроса с автоматической обработкой результата.
        """
        if not isinstance(data, dict):
            raise ValueError("Данные должны быть словарем.")
        full_url = self._build_url(url)
        response = self._request("post", full_url, json=data, headers=self.headers)

        result = {
            'success': response and response.status_code in (200, 201),
            'data': response.json() if response and response.status_code in (200, 201) else None,
            'status_code': response.status_code if response else None,
            'error': response.text if response and response.status_code not
                                      in (200, 201) else None,
            'message': response.text,
        }
        self._process_response(result, "Данные успешно отправлены.")
        return result

    def api_del(self, url):
        """
        Выполнение DELETE-запроса с автоматической обработкой результата.
        """
        full_url = self._build_url(url)
        response = self._request("delete", full_url, headers=self.headers)

        result = {
            'success': response and response.status_code in (200, 204),
            'message': f'Запись успешно удалена. {response.text}' if (response
                and response.status_code in (200, 204)) else None,
            'status_code': response.status_code if response else None,
            'error': response.text if response and response.status_code not
                                      in (200, 204) else None
        }
        self._process_response(result, "Запись успешно удалена.")
        return result

# # Регистрируем пользователя
# url = "http://127.0.0.1:8000/api/auth/registration/"
#
# data = {
#     "username": "ownerS",
#     "email": "qwertyclop@gmail.com",
#     "password1": "t2yweda14sSa32",
#     "password2": "t2yweda14sSa32"
# }
# response = requests.post(url, json=data)
# if response.status_code == 201:
#     print('Аккаунт зарегистрирован', response.text)
# else:
#     print(response.text, response.status_code)


# Создам экземпляр класса и сразу логинимся
one = BuildApi()
two = BuildApi(login='ownerS', password='t2yweda14sSa32')


