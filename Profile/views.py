from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response  # Добавьте этот импорт
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import ProfileSerializer
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

# Create your views here.


class MyProfile(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer

    permission_classes = [AllowAny]

