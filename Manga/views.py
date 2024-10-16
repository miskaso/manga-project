from django.shortcuts import render
from .models import Author, Manga, Category, Tag
from .serializers import MangaSerializer
from rest_framework import viewsets
from rest_framework.permissions import BasePermission



# Create your views here.


class IsAdminOrRead(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'DELETE']:
            return request.user.is_staff
        return True


class ShowManga(viewsets.ModelViewSet):
    queryset = Manga.objects.all()
    serializer_class = MangaSerializer

    permission_classes = [IsAdminOrRead]

class SearchView(viewsets.ModelViewSet):
    queryset = Manga.objects.filter()