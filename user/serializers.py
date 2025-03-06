from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Используется для отображения информации о пользователях."""

    class Meta:
        model = User
        fields = [
            'public_id', 'username', 'first_name',
            'last_name', 'bio', 'photo', 'email',
            'is_active'
        ]
