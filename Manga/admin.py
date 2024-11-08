from django.contrib import admin
from .models import Tag, Category, Author, Manga, ChapterModel

# Register your models here.

admin.site.register(Manga)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(ChapterModel)
