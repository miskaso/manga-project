from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Fon(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=255)
    user = models.ManyToManyField(User, related_name='fon')
    fon = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name


class Stick(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=255)
    user = models.ManyToManyField(User, related_name='stick')
    img = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name

