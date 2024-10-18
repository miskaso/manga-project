from django.db import models


# Create your models here.


class Category(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category


class Tag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag


class Author(models.Model):
    name = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    ava = models.ImageField(upload_to='images/')
    bio = models.TextField()

    def __str__(self):
        return self.name


class Manga(models.Model):
    title = models.CharField(max_length=100)
    year = models.DateField()
    description = models.TextField()
    img = models.ImageField(upload_to='images/')
    chapters = models.FileField(upload_to='files/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
