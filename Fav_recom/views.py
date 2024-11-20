from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from .models import Favorite
from .serializers import FavoriteSerializer
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
# Create your views here.


class FavoriteView(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Переопределение для автоматического добавления пользователя при
        добавлении в избранное.
        """
        manga_id = self.request.data.get('manga')  # получаем ID манги из данных запроса
        if self.queryset.filter(user=self.request.user, manga=manga_id).exists():
            raise ValidationError({"error": "Эта манга уже избрана."})

        # Если манга еще не в избранном, сохраняем запись
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        """
        Переопределение метода для удаления записи из избранного.
        Проверка, что запись принадлежит текущему пользователю.
        """
        if instance.user != self.request.user:
            raise ValidationError({"error": "Вы не можете удалить чужую запись из избранного."})

        # Удаление записи
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        """
        Переопределение стандартного метода destroy для добавления кастомного ответа.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Манга удалена из избранного'},
            status=status.HTTP_204_NO_CONTENT
        )
