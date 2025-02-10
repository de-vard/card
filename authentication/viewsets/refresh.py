from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import AllowAny
from rest_framework import status, generics
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


class RefreshViewSet(generics.CreateAPIView, TokenRefreshView):
    """
    ViewSet для обновления JWT access-токена.
    Пользователь отправляет refresh-токен, и API возвращает новый access-токен.
    """

    # Разрешаем доступ всем (не требуется аутентификация)
    permission_classes = (AllowAny,)

    # Разрешаем только метод POST, так как обновление токена выполняется через POST-запрос
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """
        Метод для обработки запроса на обновление токена.
        """
        # Создаём сериализатор и передаём в него данные запроса (refresh-токен)
        serializer = self.get_serializer(data=request.data)

        try:
            # Проверяем валидность переданного refresh-токена
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            # Если произошла ошибка при обработке токена (например, он просрочен или некорректен),
            # вызываем исключение InvalidToken, которое API вернёт с кодом 401 Unauthorized
            raise InvalidToken(e.args[0])

        # Если всё прошло успешно, возвращаем новый access-токен в ответе
        return Response(serializer.validated_data, status=status.HTTP_200_OK)