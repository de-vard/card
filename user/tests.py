import pytest
from django.contrib.auth import get_user_model

# Получаем модель пользователя, определённую в Django
User = get_user_model()

# Тестовые данные для создания пользователя
data_user = {
    "username": "test_user",
    "email": "test@gmail.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "test_password",
    "bio": "This is a test bio",
    "date_of_birth": "1990-01-01",
}


@pytest.mark.django_db  # Декоратор для работы с базой данных в тесте
def test_create_user():
    # Создаём пользователя в базе данных
    user = User.objects.create_user(**data_user)

    # Проверяем, что данные в объекте соответствуют ожидаемым значениям
    assert user.username == data_user["username"]
    assert user.email == data_user["email"]
    assert user.first_name == data_user["first_name"]
    assert user.last_name == data_user["last_name"]
    assert user.bio == data_user["bio"]
    assert str(user.date_of_birth) == str(data_user["date_of_birth"])  # Проверка даты

    assert user.public_id is not None  # Проверяем, что public_id был создан
    assert user.is_active is True  # Проверяем статус активности пользователя

    # Проверяем, что сгенерированный public_id — уникальный UUID
    another_user = User.objects.create_user(username="test_user_2", email="test2@gmail.com", password="test_password")
    assert user.public_id != another_user.public_id  # Проверка на уникальность public_id
