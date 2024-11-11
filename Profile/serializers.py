from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Notification, Role, UserRole


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']


class UserRoleSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = UserRole
        fields = ['user', 'role']


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        extra_kwargs = {'password': {'write_only': True}, 'username': {'write_only': True}}

    def create(self, validated_data):
        password1 = validated_data.pop('password1')
        password2 = validated_data.pop('password2')

        if password1 != password2:
            raise serializers.ValidationError({"Ошибка": "Пароли не совпадают."})

        user = User(**validated_data)
        user.set_password(password1)
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    name = UserSerializer()

    class Meta:
        model = Profile
        fields = ['name', 'bio', 'year']

    def create(self, validated_data):
        user_data = validated_data.pop('name')  # Извлекаем данные для пользователя
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)  # Создаем пользователя
        profile = Profile.objects.create(name=user, **validated_data)  # Создаем профиль
        return profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop('name', None)  # Извлекаем данные для пользователя
        if user_data:
            user_serializer = UserSerializer(instance.name, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)

            if 'password' in user_data:
                instance.name.set_password(user_data['password'])

            if 'email' in user_data:
                instance.name.email = user_data['email']

            user_serializer.save()  # Сохраняем изменения пользователя

        # Обновляем поля профиля
        instance.bio = validated_data.get('bio', instance.bio)
        instance.year = validated_data.get('year', instance.year)
        instance.save()  # Сохраняем изменения профиля
        return instance


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['manga.title', 'description', 'data']
