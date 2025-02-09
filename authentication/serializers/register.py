from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.serializers import UserSerializer

User = get_user_model()


class RegisterSerializer(UserSerializer):
    """Сериализатор для регистрации запросов и создания пользователя"""

    # Убедимся, что пароль не короче 8 символов, не длиннее 128 и не может быть прочитан пользователем
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'bio', 'photo', 'email', 'username', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        # Используем метод `create_user`, который мы написали ранее для UserManager, чтобы создать нового пользователя.
        return User.objects.create_user(**validated_data)
