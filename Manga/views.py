from django.shortcuts import render
from .models import Author, Manga, Category, Tag
from .serializers import MangaSerializer, SearchSerializer
from rest_framework import viewsets
from rest_framework.permissions import BasePermission
from django.db.models import Q

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
    serializer_class = SearchSerializer
    queryset = Manga.objects.all()

    def get_queryset(self):
        manga = self.request.query_params.get('title')
        author = self.request.query_params.get('author')
        year = self.request.query_params.get('year')
        tags = self.request.query_params.get('tags')
        category = self.request.query_params.get('category')

        filters = Q()

        if manga:
            filters &= Q(title__icontains=manga)
        if author:
            filters &= Q(author__icontains=author)
        if year:
            filters &= Q(year__year=year)
        if tags:
            filters &= Q(tags__icontains=tags)
        if category:
            filters &= Q(category__icontains=category)

        # Если фильтры не заданы, возвращаем все результаты
        if filters:
            queryset = queryset.filter(filters)

        return queryset
