from Reviews.models import Popular
from django.db.models import Q, F
from rest_framework import viewsets
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Manga, Author, Category, Tag, ChapterModel
from .serializers import (MangaSerializer, AuthorSerializer,
                          CategorySerializer, TagSerializer, ChapterSerializer)


# Создаем класс для редакта админам и просмотра обычным юзерам
class IsAdminOrRead(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'DELETE']:
            return request.user.is_staff
        return True


# Создаем вьюшку для отображения, фильтрации и учета манги.
class SearchView(viewsets.ModelViewSet):
    serializer_class = MangaSerializer
    queryset = Manga.objects.all()
    permission_classes = [IsAdminOrRead]

    # При детальном просмотре конкретной манги обновляем счетчик популярности
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.popularity += 1
        instance.save(update_fields=['popularity'])
        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    # Фильтрация и подсчет рейтинга.
    def get_queryset(self):
        manga = self.request.query_params.get('title')
        author = self.request.query_params.get('author')
        year = self.request.query_params.get('year')
        tags = self.request.query_params.get('tags')
        category = self.request.query_params.get('category')
        top = self.request.query_params.get('top')
        new = self.request.query_params.get('new')

        queryset = super().get_queryset()

        # Фильтрация по новизне
        if new:
            queryset = queryset.order_by('-id')
            return queryset

        filters = []

        # Фильтрация по параметрам
        if manga:
            filters.append(Q(title__icontains=manga))
        if author:
            filters.append(Q(author__name__icontains=author))
        if year:
            filters.append(Q(year__year=year))
        if tags:
            filters.append(Q(tags__tag__icontains=tags))
        if category:
            filters.append(Q(category__category__icontains=category))

        if filters:
            combined_filters = Q()
            for condition in filters:
                combined_filters &= condition
            queryset = queryset.filter(combined_filters)
        else:
            # Рассчет рейтинга и аннотирование
            queryset = queryset.annotate(
                calculated_rating=(
                    F('average_rating') * 0.5 +
                    F('rating_count') * 0.2 +
                    F('popularity') * 0.3
                )
            ).order_by('-calculated_rating')

            # Обновление значений top
            for index, manga in enumerate(queryset, start=1):
                if manga.top != index:
                    manga.top = index
                    manga.save(update_fields=['top'])

            # Фильтрация по top, если указан
            if top:
                queryset = queryset.filter(top=int(top))
            else:
                queryset = queryset.order_by('top')

        return queryset


# вьюшка для отображения списка авторов и их детального просмотра
class AuthorView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    permission_classes = [IsAdminOrRead]

    def get_queryset(self):
        name = self.request.query_params.get('name')
        lastname = self.request.query_params.get('lastname')

        queryset = super().get_queryset()

        filters = []
        if name:
            filters.append(Q(name__icontains=name))
        if lastname:
            filters.append(Q(lastname__icontains=lastname))

        if filters:
            combined_filters = Q()
            for condition in filters:
                combined_filters &= condition
            queryset = queryset.filter(combined_filters)

        return queryset


# Вьюшка под вывод категорий
class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    permission_classes = [IsAdminOrRead]

    def get_queryset(self):
        category = self.request.query_params.get('category')

        queryset = super().get_queryset()

        filters = []
        if category:
            filters.append(Q(category__icontains=category))

        if filters:
            combined_filters = Q()
            for condition in filters:
                combined_filters &= condition
            queryset = queryset.filter(combined_filters)

        return queryset


# вьюшка под теги
class TagsView(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    permission_classes = [IsAdminOrRead]

    def get_queryset(self):
        tag = self.request.query_params.get('tag')

        queryset = super().get_queryset()

        filters = []

        if tag:
            filters.append(Q(tag__icontains=tag))

        if filters:
            combined_filters = Q()
            for condition in filters:
                combined_filters &= condition
            queryset = queryset.filter(combined_filters)

        return queryset


class ChapterView(viewsets.ModelViewSet):
    queryset = ChapterModel.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [IsAdminOrRead]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Проверка, является ли глава премиум
        if instance.premium:
            # Проверка, состоит ли пользователь в группе 'premium'
            if not self.request.user.groups.filter(name='premium').exists():
                raise PermissionDenied(
                    'У вас недостаточно прав для просмотра этой главы.')

        # Если доступ есть, отправляем данные
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        title = self.request.query_params.get('title')
        manga = self.request.query_params.get('manga')
        premium = self.request.query_params.get('premium')
        date = self.request.query_params.get('date')

        queryset = super().get_queryset()

        # Фильтрация глав
        filters = Q()

        if title:
            filters &= Q(title__icontains=title)
        if manga:
            filters &= Q(manga__icontains=manga)
        if premium:
            filters &= Q(premium=premium)
        if date:
            filters &= Q(data__icontains=date)

        return queryset.filter(filters) if filters else queryset
