from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from authentication.serializers.register import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        # Создание экземпляра сериализатора
        serializer = self.serializer_class(data=request.data)

        # Проверка на валидность данных
        serializer.is_valid(raise_exception=True)

        # Сохранение пользователя
        user = serializer.save()

        # Генерация токенов
        refresh = RefreshToken.for_user(user)

        # Формирование ответа с токенами
        return Response({
            "user": serializer.data,
            "refresh": str(refresh),
            "token": str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)
