from django.db import models
from django.contrib.auth.models import User
from Manga.models import Manga

# Create your models here.


class Profile(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    year = models.IntegerField()
    avatar = models.ImageField(upload_to='images/')
    fon = models.ImageField(upload_to='images/')

    def __str__(self):
        return f'{self.name}'


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, default='Вышла новая глава!')
    data = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Уведомление для {self.user.username} о манге {self.manga.title}"



