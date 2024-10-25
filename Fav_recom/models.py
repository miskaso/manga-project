from Manga.models import Manga
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Favorite(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    manga_id = models.ForeignKey(Manga, on_delete=models.CASCADE)


