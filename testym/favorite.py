import func
# Приложение: Фавориты

# Получаем экземпляр
one = func.one

# Добавить в избранные мангу
# data = {
#     'user': 11,
#     'manga': 2
# }
# one.api_post(data, '/fav_recom/favorite/')

# Получить избранные
one.api_get('/fav_recom/favorite/')

# Удалить из избранного
# one.api_del('/fav_recom/favorite/1/')