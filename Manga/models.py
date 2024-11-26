from django.db import models


# Create your models here.

# Модель категорий
class Category(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category


# Модель тегов
class Tag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag


# Модель авторов
class Author(models.Model):
    name = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    ava = models.ImageField(upload_to='images/')
    bio = models.TextField()

    def __str__(self):
        return f'{self.name}'


# модель манги
class Manga(models.Model):
    title = models.CharField(max_length=100)
    year = models.DateField()
    description = models.TextField()
    img = models.ImageField(upload_to='images/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    top = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    rating_count = models.IntegerField(default=0)
    popularity = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title}'


# Модель глав манги
class ChapterModel(models.Model):
    title = models.CharField(max_length=255)
    data = models.DateTimeField(auto_now=True)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    content = models.FileField(upload_to='files/')
    premium = models.BooleanField()

    def __str__(self):
        return f'{self.title}, {self.manga}'

