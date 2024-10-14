from .models import Author, Category, Tag, Manga
from rest_framework import serializers


class MangaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manga
        fields = '__all__'

