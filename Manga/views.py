from Reviews.models import Popular
from django.db.models import Q, F
from rest_framework import viewsets
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from .models import Manga
from .serializers import MangaSerializer


# Create your views here.


# Создаем класс для редакта админам и просмотра обычным юзерам
class IsAdminOrRead(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'DELETE']:
            return request.user.is_staff
        return True


class SearchView(viewsets.ModelViewSet):
    serializer_class = MangaSerializer
    queryset = Manga.objects.all()
    permission_classes = [IsAdminOrRead]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.popularity += 1
        instance.save(update_fields=['popularity'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

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

