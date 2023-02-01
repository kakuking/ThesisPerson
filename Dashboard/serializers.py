from rest_framework import serializers
from .models import Light, TelegramUser

class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = '__all__'


class LightSerializer(serializers.ModelSerializer):
    registeredUsers = TelegramUserSerializer(many=True, read_only=True)
    class Meta:
        model = Light
        fields = '__all__'
