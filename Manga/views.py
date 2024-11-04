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
        instance.save(update_fields=['popularity'])  # Оптимизация сохранения
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        manga = self.request.query_params.get('title')
        author = self.request.query_params.get('author')
        year = self.request.query_params.get('year')
        tags = self.request.query_params.get('tags')
        category = self.request.query_params.get('category')
        top = self.request.query_params.get('top')

        queryset = super().get_queryset()
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

        # Рассчет рейтинга и аннотирование
        queryset = queryset.annotate(
            calculated_rating=(
                F('average_rating') * 0.5 +
                F('rating_count') * 0.2 +
                F('popularity') * 0.3
            )
        )

        # Фильтрация по рейтингу, если задан параметр top
        if top:
            str(top)
            if top == '':
                queryset = queryset.filter(calculated_rating__gte=top)
                # Сортировка по рассчитанному рейтингу
                queryset = queryset.order_by('-calculated_rating')
                return queryset
            else:
                try:
                    queryset = queryset.filter(top=top)
                except ValueError:
                    queryset = queryset.filter(top=top)
        return queryset

