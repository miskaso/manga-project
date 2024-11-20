from Manga.models import Manga
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)

    def __str__(self):
        return f'Юзер: {self.user}, Манга: {self.manga}'

