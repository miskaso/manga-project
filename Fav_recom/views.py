from django.shortcuts import render
from .models import Favorite
from .serializers import FavoriteSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
# Create your views here.


class FavoriteView(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    permission_classes = [AllowAny]

    def get_queryset(self):
        return self.queryset

