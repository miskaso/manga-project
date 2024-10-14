from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import ProfileSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

# Create your views here.


class MyProfile(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer

    permission_classes = [AllowAny]


class Register(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [AllowAny]


