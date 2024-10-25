from Manga.models import Manga
from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    message = models.TextField()
    choices = [
        (1, '1 звезда'),
        (2, '2 звезды'),
        (3, '3 звезды'),
        (4, '4 звезды'),
        (5, '5 звезд'),
    ]
    rating = models.IntegerField(choices=choices)

    class Meta:
        unique_together = ('user', 'manga')  # Ограничение на уникальность

    def __str__(self):
        return self.message[:50]  # Первые 50 символов сообщения


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)

    def __str__(self):
        return f'Манга: {self.manga}, Юзер: {self.user}'


class Popular(models.Model):
    manga = models.OneToOneField(Manga, on_delete=models.CASCADE)
    check_count = models.IntegerField()

    def __str__(self):
        return f'{self.manga}, {self.check_count}'

