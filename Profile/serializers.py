from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['name', 'bio', 'year', 'user']

    def create(self, validated_data):
        name_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(name=user, **name_data)

        return user

