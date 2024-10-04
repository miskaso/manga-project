from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField()
    avatar = models.ImageField()
    fon = models.ImageField()

    def __str__(self):
        return self.name


class Notification(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    manga_id = models.IntegerField()
    description = models.CharField(max_length=100, default='Вышла новая глава!')
