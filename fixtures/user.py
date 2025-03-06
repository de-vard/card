import pytest
from django.contrib.auth import get_user_model

# Получаем модель пользователя, определённую в Django
User = get_user_model()

# Данные для создания пользователя
data_user = {
    "username": "test_user",
    "email": "test@gmail.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "test_password",
    "bio": "This is a test bio",
    "date_of_birth": "1990-01-01",
}
data_author = {
    "username": "test_author",
    "email": "test_author@gmail.com",
    "first_name": "Test_author",
    "last_name": "Author",
    "password": "test_password22",
    "bio": "This is a test bio222",
    "date_of_birth": "1994-01-01",
}


# Фикстура для создания пользователя перед тестом
@pytest.fixture
def user(db) -> User:
    return User.objects.create_user(**data_user)


# Фикстура для создания пользователя перед тестом
@pytest.fixture
def author(db) -> User:
    return User.objects.create_user(**data_author)
