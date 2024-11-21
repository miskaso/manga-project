import func
# Приложение: Манга


# Получаем наш экземпляр
one = func.one


# # Получить список манги
# one.api_get('/manga/show/')
#
# # ПОлучить рекомендации по манге
# one.api_get('/manga/show/?recom/')
#
# # Отфильтровать мангу
# one.api_get('/manga/show/?author=Ктото&category=Комедия')
#
# # Для сортировки по новизне отправить new=1
# one.api_get('?new=1')
#
# # Для сортировки по топу отправить пустой top
# one.api_get('?top')
#
# # Получить авторов
# one.api_get('/manga/authors/')
#
# # Получить существующие категории
# one.api_get('/manga/categories/')

# # Добавить категорию
# data = {
#     'category': 'Приключения'
# }
# one.api_post(data, '/manga/categories/')

# Получить конкретную категорию
# one.api_get('/manga/categories/?category=Приключения')

# Получить теги
# one.api_get('/manga/tags/')

# Добавить новый тег
# data = {
#     'tag': 'Комедия'
# }
# one.api_post(data, '/manga/tags/')

# Удалить тег
# one.api_del('/manga/tags/1/')


