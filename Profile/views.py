from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from .models import Profile, Notification, Role
from .serializers import ProfileSerializer, UserSerializer, RoleSerializer
from Manga.models import Manga, ChapterModel
from Fav_recom.models import Favorite
from django.dispatch import receiver
from django.db.models.signals import post_save
from .permissions import HasRolePermission


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    permission_classes = [HasRolePermission]


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


class MyProfile(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer

    permission_classes = [AllowAny]


class ProfileView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Profile.objects.all()

    def get(self, request, *args, **kwargs):
        profiles = self.get_queryset()
        serializer = self.serializer_class(profiles, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Register(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [AllowAny]


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

