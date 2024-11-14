from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from .models import Profile, Notification
from .serializers import ProfileSerializer, UserSerializer
from Manga.models import Manga, ChapterModel
from Fav_recom.models import Favorite
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound


# Редактирование групп у пользователей
class AssignGroupView(APIView):
    # Ограничиваем доступ только для администраторов
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        group_name = request.data.get("group")

        try:
            # Получаем пользователя по имени
            user = User.objects.get(username=username)

            # Получаем группу по имени
            group = Group.objects.get(name=group_name)

            # Добавляем пользователя в группу
            user.groups.add(group)

            return Response(
                {"Сообщение": "Группа успешно назначена пользователю."},
                status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({"Ошибка": "Неизвестный пользователь."},
                            status=status.HTTP_404_NOT_FOUND)

        except Group.DoesNotExist:
            return Response({"Ошибка": "Такой группы не существует."},
                            status=status.HTTP_404_NOT_FOUND)


# Функция создания уведомлений на подписанную мангу
@receiver(post_save, sender=ChapterModel)
def create_chapter_notification(sender, instance, created, **kwargs):
    if created:
        manga = instance.manga  # Получаем мангу, к которой относится эта глава
        # Получаем список пользователей, подписанных на эту мангу
        users = Favorite.objects.filter(manga=manga).values_list('user', flat=True)
        # Перебираем всех подписанных пользователей и создаём для них уведомления
        for user_id in users:
            user = User.objects.get(id=user_id)
            # Создаём уведомление для каждого подписчика
            Notification.objects.create(
                user=user,
                manga=manga,
                description=f'Вышла новая глава "{instance.title}" в манге "{manga.title}".'
            )


# Создание профиля
class MyProfile(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer

    permission_classes = [IsAuthenticated]


# росмотр профиля и его редактирование
class ProfileView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, user):
        return Profile.objects.filter(name=user).first()

    def get(self, request, *args, **kwargs):
        # Получаем пользователя, чей профиль нужно показать
        if 'username' in kwargs:
            user = get_object_or_404(User, username=kwargs['username'])
        else:
            user = request.user  # Если не передан username, показываем профиль текущего пользователя

        profile = self.get_queryset(user)
        if not profile:
            return Response({"error": "Profile not found."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(profile)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # Проверка, существует ли уже профиль для текущего пользователя
        profile = self.get_queryset(request.user)

        if profile:
            # Если профиль существует, проверяем, что запрос отправляет сам владелец
            if profile.name != request.user:
                return Response(
                    {"error": "You can only edit your own profile."},
                    status=status.HTTP_403_FORBIDDEN)

            # Если профиль существует, редактируем его
            serializer = self.serializer_class(profile, data=request.data,
                                               partial=True)
            if serializer.is_valid():
                serializer.save()  # Обновляем профиль
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        # Если профиль не существует, создаем новый
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(name=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Регистрация
class Register(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [AllowAny]


# Выход из вккаунта путем обновления токена и занесения старого в черный список
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

