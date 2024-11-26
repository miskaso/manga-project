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
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.decorators import api_view


class BuyPremium(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        profile = Profile.objects.get(name=user)
        if user.groups.filter(name='premium').exists():
            raise ValidationError({"error": "У вас уже есть премиум подписка."})

        # Проверяем баланс
        if profile.money < 500:
            raise ValidationError({"error": "Недостаточно монет"})


        try:
            # Получаем группу 'premium'
            group = Group.objects.get(name='premium')
        except Group.DoesNotExist:
            return Response({"error": "Группа 'premium' не найдена"}, status=status.HTTP_404_NOT_FOUND)

        # Списываем монеты
        profile.money -= 500
        profile.save()

        # Добавляем пользователя в группу
        user.groups.add(group)

        return Response(
            {"message": "Вы успешно купили премиум доступ."},
            status=status.HTTP_201_CREATED
        )


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


# Просмотр профиля и его редактирование
class ProfileView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, user):

        return Profile.objects.filter(name=user).first()

    def get(self, request, *args, **kwargs):

        if 'username' in kwargs:
            user = get_object_or_404(User, username=kwargs['username'])
        else:
            user = request.user  # Профиль текущего пользователя

        profile = self.get_queryset(user)
        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(profile)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Создает или обновляет профиль текущего пользователя.
        """
        user = request.user
        profile = self.get_queryset(user)

        if profile:
            # Обновление существующего профиля
            serializer = self.serializer_class(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()  # Сохраняем изменения профиля
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Создание нового профиля
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifySMSView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('telephone')
        code = request.data.get('code')

        if not phone_number or not code:
            raise ValidationError({"Ошибка": "Телефон или код не могут быть пустыми."})

        try:
            profile = Profile.objects.get(telephone=phone_number)
        except Profile.DoesNotExist:
            raise NotFound({"Ошибка": "Такого пользователя не существует."})

        if profile.verification_token != code:
            raise ValidationError({"Ошибка": "Неверный код."})

        profile.verification = True
        profile.verification_token = None
        profile.save()

        return Response({"message": "Phone number successfully verified."}, status=status.HTTP_200_OK)


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


@api_view(['POST'])
def pay_account(request):
    # Извлекаем 'money' из тела запроса
    money = request.data.get('money')

    if not money or not str(money).isdigit():
        return Response({'error': 'Некорректная сумма'}, status=400)

    money = int(money)  # Преобразуем в число

    # Получаем профиль текущего пользователя
    profile = get_object_or_404(Profile, name=request.user.id)

    # Обновляем баланс
    profile.money += money
    profile.save()

    return Response({'message': 'Баланс обновлен'}, status=200)
