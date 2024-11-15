from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Notification
import random
from twilio.rest import Client
from django.conf import settings


def generate_verification_code():
    return str(random.randint(100000, 999999))


def send_verification_sms(phone_number, code):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_phone_number = settings.TWILIO_PHONE_NUMBER

    client = Client(account_sid, auth_token)
    try:
        message = client.messages.create(
            body=f"Ваш код для верификации: {code}",
            from_=twilio_phone_number,
            to=phone_number
        )
        print(f"SMS sent to {phone_number}. SID: {message.sid}")
    except Exception as e:
        print(f"Failed to send SMS: {e}")
        raise Exception("Failed to send SMS")


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
    class Meta:
        model = Profile
        fields = ['bio', 'year', 'telephone']

    def create(self, validated_data):
        """
        Создает профиль текущего пользователя.
        """
        # Извлекаем текущего пользователя из контекста
        user = self.context['request'].user

        # Удаляем из данных возможный конфликтующий аргумент 'name'
        validated_data.pop('name', None)

        # Генерируем верификационный код (если нужно)
        verification_code = generate_verification_code()

        # Создаем профиль
        profile = Profile.objects.create(
            name=user,
            verification_token=verification_code,
            **validated_data
        )

        # Отправляем SMS с кодом
        send_verification_sms(profile.telephone, verification_code)

        return profile


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['manga.title', 'description', 'data']
