from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User


class UserMeSerializer(UserSerializer):
    """Сериализатор для текущего пользователя."""
    role = serializers.CharField(read_only=True)


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации."""
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                "Использовать имя _me_ в качестве username запрещено."
            )
        return value

    class Meta:
        fields = ('email', 'username')
        model = User


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        user = get_object_or_404(User, username=data.get('username'))
        confirmation_code = data.get('confirmation_code')
        if default_token_generator.check_token(user, confirmation_code):
            return data
        raise serializers.ValidationError('Неверный проверочный код.')
