from django.shortcuts import render
from .serializers import PopularSerializer, CommentSerializer, ReviewSerializer
from .models import Popular, Comment, Review
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import Group
from django.db.models import Q, F
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import BasePermission


# разрешения и права для комментариев
class CanEditOrDeleteComment(BasePermission):
    def has_permission(self, request, view):
        """
        Разрешение для редактирования и удаления комментариев.
        Проверка, является ли пользователь владельцем комментария,
        администратором или модератором.
        """
        # Разрешаем просмотр комментариев всем пользователям (GET-запрос)
        if request.method == 'GET':
            return True

        # Получаем объект комментария для редактирования или удаления
        comment = view.get_object()

        # Разрешаем редактировать/удалять владельцу
        if comment.user == request.user:
            return True

        # Разрешаем редактировать/удалять администраторам и модераторам
        if request.user.groups.filter(name='admins').exists() or request.user.groups.filter(name='moderators').exists():
            return True

        return False


# Работа с комментариями, создание удаление редакт
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [CanEditOrDeleteComment]

    def perform_create(self, serializer):
        # Привязываем комментарий к текущему пользователю при его создании
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Фильтруем комментарии
        user = self.request.query_params.get('user')
        manga = self.request.query_params.get('manga')
        id = self.request.query_params.get("id")
        user_id = self.request.query_params.get('user_id')
        manga_id = self.request.query_params.get('manga_id')

        queryset = Comment.objects.all()

        # поиск конкретного коммента
        if id:
            queryset = queryset.filter(id=id)
            return queryset

        filters = []
        if user:
            filters.append(Q(user__username__icontains=user))  # Фильтрация по имени пользователя
        if user_id:
            filters.append(
                Q(user__id=user_id))  # Фильтрация по ID пользователя

        if manga_id:
            filters.append(
                Q(manga__id=manga_id))  # Фильтрация по ID манги
        if manga:
            filters.append(Q(manga__title__icontains=manga))  # Фильтрация по названию манги

        if filters:
            combined_filters = Q()
            for condition in filters:
                combined_filters &= condition
            queryset = queryset.filter(combined_filters)

        # Если фильтры не применены, получаем комментарии текущего пользователя
        if not filters:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_object(self):
        # Получаем комментарий
        comment = super().get_object()
        # Проверяем, что пользователь владеет комментом
        if comment.user != self.request.user:
            raise PermissionDenied("У вас нет прав для редактирования этого комментария.")
        return comment

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]  # Открыто для всех для просмотра
        return [IsAuthenticated()]  # Для других методов необходима авторизация

    def perform_destroy(self, instance):
        # Проверяем, что пользователь является администратором, модератором или владельцем комментария
        if not self.request.user.is_staff and not self.request.user.groups.filter(name='moderators').exists() and instance.user != self.request.user:
            raise PermissionDenied("У вас нет прав для удаления этого комментария.")
        # Удаляем комментарий
        instance.delete()

    # Для метода удаления комментария (destroy)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Получаем комментарий
        self.perform_destroy(instance)  # Удаляем комментарий с проверкой прав
        return Response(status=status.HTTP_204_NO_CONTENT)  # Возвращаем ответ с кодом 204


class ReviewView(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Привязываем отзыв к текущему пользователю при его создании
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Фильтруем отзывы
        user = self.request.query_params.get('user')
        manga = self.request.query_params.get('manga')
        id = self.request.query_params.get("id")
        rating = self.request.query_params.get('rating')
        user_id = self.request.query_params.get('user_id')
        manga_id = self.request.query_params.get('manga_id')

        queryset = Review.objects.all()

        # поиск конкретного коммента
        if id:
            queryset = queryset.filter(id=id)
            return queryset

        filters = []
        if user:
            filters.append(
                Q(user__username__icontains=user))  # Фильтрация по имени пользователя
        if user_id:
            filters.append(
                Q(user__id=user_id))  # Фильтрация по ID пользователя

        if manga:
            filters.append(
                Q(manga__title__icontains=manga))  # Фильтрация по названию манги
        if manga_id:
            filters.append(
                Q(manga__id=manga_id))  # Фильтрация по ID манги

        if rating:
            filters.append(
                Q(rating__icontains=rating))  # Фильтрация по оценке

        if filters:
            combined_filters = Q()
            for condition in filters:
                combined_filters &= condition
            queryset = queryset.filter(combined_filters)

        # Если фильтры не применены, получаем отзывы текущего пользователя
        if not filters:
            queryset = queryset.filter(user=self.request.user)

        return queryset

    def get_object(self):
        # Получаем отзыв
        comment = super().get_object()
        # Проверяем, что пользователь владеет отзывом
        if comment.user != self.request.user:
            raise PermissionDenied(
                "У вас нет прав для редактирования этого отзыва.")
        return comment

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]  # Открыто для всех для просмотра
        return [IsAuthenticated()]  # Для других методов необходима авторизация

    def perform_destroy(self, instance):
        # Проверяем, что пользователь является администратором, модератором или владельцем комментария
        if not self.request.user.is_staff and not self.request.user.groups.filter(
                name='moderators').exists() and instance.user != self.request.user:
            raise PermissionDenied(
                "У вас нет прав для удаления этого комментария.")
        # Удаляем отзыв
        instance.delete()

    # Для метода удаления отзыва (destroy)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Получаем отзыв
        self.perform_destroy(instance)  # Удаляем отзыв с проверкой прав
        return Response(
            status=status.HTTP_204_NO_CONTENT)  # Возвращаем ответ с кодом 204


class PopularView(viewsets.ReadOnlyModelViewSet):
    queryset = Popular.objects.all()
    serializer_class = PopularSerializer

    permission_classes = [AllowAny]

