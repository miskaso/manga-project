from .models import Author, Category, Tag, Manga, ChapterModel
from rest_framework import serializers


class MangaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manga
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChapterModel
        exclude = ['data']
