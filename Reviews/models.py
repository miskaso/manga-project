from Manga.models import Manga
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Review(models.Model):
    title = models.CharField(max_length=255)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    manga_id = models.ForeignKey(Manga, on_delete=models.CASCADE)
    message = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    manga_id = models.ForeignKey(Manga, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)

    def __str__(self):
        return f' Манга: {self.manga_id}, Юзер: {self.user_id}'
