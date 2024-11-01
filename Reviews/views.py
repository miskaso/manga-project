from django.shortcuts import render
from .serializers import PopularSerializer, CommentSerializer, ReviewSerializer
from .models import Popular, Comment, Review
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
# Create your views here.


class CommentsView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print('Вызов функции')
        serializer.save(user=self.request.user)


class ReviewView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print('Вызов функции')
        serializer.save(user=self.request.user)


class PopularView(viewsets.ReadOnlyModelViewSet):
    queryset = Popular.objects.all()
    serializer_class = PopularSerializer

    permission_classes = [AllowAny]

