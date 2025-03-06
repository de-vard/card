import pytest
from rest_framework import status
from fixtures.user import user


class TestAuthenticationViewSet:
    # Определяем базовый URL для тестирования аутентификации
    endpoint = '/api/v1/authentication/'

    def test_login(self, client, user):
        # Создаем данные для теста: логин и пароль
        data = {
            "username": user.username,  # Имя пользователя из фикстуры
            "password": "test_password"  # Пароль пользователя для теста
        }

        # Отправляем POST-запрос на эндпоинт логина с данными пользователя
        response = client.post(self.endpoint + "login/", data)

        # Проверяем, что код состояния ответа равен 200 OK, что означает успешный запрос
        assert response.status_code == status.HTTP_200_OK

        # Проверяем, что в ответе есть ключ 'access', который указывает на наличие access токена
        assert response.data['access']

        # Проверяем, что public_id пользователя в ответе совпадает с его public_id в базе данных
        assert response.data['user']['public_id'] == str(user.public_id)

        # Проверяем, что имя пользователя в ответе совпадает с его именем в базе данных
        assert response.data['user']['username'] == user.username

        # Проверяем, что email пользователя в ответе совпадает с его email в базе данных
        assert response.data['user']['email'] == user.email

    @pytest.mark.django_db
    def test_register(self, client):
        # Создаем данные для регистрации нового пользователя
        data = {
            "username": "johndoe",  # Имя пользователя для нового аккаунта
            "email": "johndoe@yopmail.com",  # Электронная почта нового пользователя
            "password": "test_password",  # Пароль для нового пользователя
            "first_name": "John",  # Имя нового пользователя
            "last_name": "Doe"  # Фамилия нового пользователя
        }
        # Отправляем POST-запрос для регистрации нового пользователя
        response = client.post(self.endpoint + "register/", data)

        # Проверяем, что код состояния ответа равен 201 CREATED, что означает успешную регистрацию
        assert response.status_code == status.HTTP_201_CREATED

    def test_refresh(self, client, user):
        # Создаем данные для теста: логин и пароль пользователя
        data = {
            "username": user.username,
            "password": "test_password"  # Пароль пользователя для теста
        }
        # Отправляем POST-запрос для логина и получения токенов
        response = client.post(self.endpoint + "login/", data)

        # Проверяем, что код состояния ответа равен 200 OK, что означает успешный запрос
        assert response.status_code == status.HTTP_200_OK

        # Создаем данные для обновления токена (используем refresh токен из ответа)
        data_refresh = {
            "refresh": response.data['refresh']  # Используем refresh токен для получения нового access токена
        }
        # Отправляем POST-запрос для получения нового access токена
        response = client.post(self.endpoint + "refresh/", data_refresh)

        # Проверяем, что код состояния ответа равен 200 OK
        assert response.status_code == status.HTTP_200_OK

        # Проверяем, что в ответе есть новый access токен
        assert response.data['access']
