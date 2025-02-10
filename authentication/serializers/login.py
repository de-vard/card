from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login

from user.serializers import UserSerializer


class LoginSerializer(TokenObtainPairSerializer):
    """
    Кастомный сериализатор для входа в систему (авторизации) с JWT.
    Наследуется от стандартного TokenObtainPairSerializer и расширяет его,
    добавляя данные пользователя в ответ.
    """

    def validate(self, attrs):
        """
        Проверяет входные данные (логин и пароль), создает JWT-токены
        и добавляет в ответ информацию о пользователе.
        """
        # Вызываем стандартную проверку логина/пароля и получаем access и refresh токены
        data = super().validate(attrs)

        # Получаем refresh-токен для пользователя
        refresh = self.get_token(self.user)

        # Добавляем в ответ сериализованные данные пользователя
        data['user'] = UserSerializer(self.user).data

        # Добавляем refresh и access токены в ответ
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Если в настройках SIMPLE_JWT включено обновление времени последнего входа
        if api_settings.UPDATE_LAST_LOGIN:
            # Обновляем поле last_login в базе данных для пользователя
            update_last_login(None, self.user)

        # Возвращаем финальный ответ с токенами и данными пользователя
        return data
