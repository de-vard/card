from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status, generics
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from authentication.serializers.login import LoginSerializer


class LoginView(generics.CreateAPIView):
    """
    ViewSet для обработки входа в систему (логина) с использованием JWT.
    Позволяет пользователям аутентифицироваться, отправляя логин и пароль.
    В ответе возвращает access/refresh токены и данные пользователя.
    """

    # Указываем, что используем LoginSerializer для обработки данных
    serializer_class = LoginSerializer

    # Разрешаем доступ любым пользователям (даже неавторизованным)
    permission_classes = (AllowAny,)

    # Разрешаем только метод POST (логин)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """
        Обрабатывает POST-запрос на вход в систему.
        Проверяет логин и пароль, выдает access и refresh токены.
        """
        # Создаем экземпляр LoginSerializer и передаем в него данные запроса
        serializer = self.serializer_class(data=request.data)

        try:
            # Проверяем валидность введенных данных (логин/пароль)
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            # Если произошла ошибка при создании токена (например, неверные данные),
            # выбрасываем исключение InvalidToken, которое API превратит в 401 Unauthorized
            raise InvalidToken(e.args[0])

        # Если валидация успешна, возвращаем ответ с токенами и данными пользователя
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
