from django.shortcuts import render
from .models import Author, Manga, Category, Tag
from .serializers import MangaSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

# Create your views here.


class ShowManga(viewsets.ModelViewSet):
    queryset = Manga.objects.all()
    serializer_class = MangaSerializer

    permission_classes = [AllowAny]
