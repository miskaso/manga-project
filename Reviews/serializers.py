from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Review, Comment, Popular


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['manga', 'rating', 'message']


class PopularSerializer(serializers.ModelSerializer):
    class Meta:
        model = Popular
        fields = '__all__'
