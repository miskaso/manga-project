from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import BasePermission

from .models import Manga
from .serializers import MangaSerializer
from Reviews.models import Popular

# Create your views here.


# Создаем класс для редакта админам и просмотра обычным юзерам
class IsAdminOrRead(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'DELETE']:
            return request.user.is_staff
        return True


# просмотр тайтлов и поиск
class SearchView(viewsets.ModelViewSet):
    serializer_class = MangaSerializer
    queryset = Manga.objects.all()
    permission_classes = [IsAdminOrRead]

    def get_queryset(self):
        manga = self.request.query_params.get('title')
        author = self.request.query_params.get('author')
        year = self.request.query_params.get('year')
        tags = self.request.query_params.get('tags')
        category = self.request.query_params.get('category')
        popular = self.request.query_params.get('popular')

        popular_obj = Popular.objects.all()

        queryset = super().get_queryset()
        filters = Q()

        if manga:
            filters &= Q(title__icontains=manga)
        if author:
            filters &= Q(author__name__icontains=author)
        if year:
            filters &= Q(year__year=year)
        if tags:
            filters &= Q(tags__tag__icontains=tags)
        if category:
            filters &= Q(category__category__icontains=category)

        # Если фильтры не заданы, возвращаем все результаты
        if filters:
            queryset = queryset.filter(filters).order_by('desc')

        if popular:
            filters &= Q(popular__popular__icontains=popular)
            queryset = popular_obj.filter(filters).order_by('desc')

        return queryset
