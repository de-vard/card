from rest_framework import status

from course.models import RegisteredUsers
# Импортируем фикстуры для пользователя, автора и курса
from fixtures.user import user, author
from fixtures.course import course


class TestCourseViewSet:
    # Определяем endpoint для работы с курсами
    endpoint = '/api/v1/courses/'

    def test_list(self, client, author, course):
        """Тест на получение списка курсов авторизованным пользователем"""
        # Авторизуем пользователя
        client.force_authenticate(user=author)

        # Отправляем GET-запрос на список курсов
        response = client.get(self.endpoint)

        # Проверяем, что ответ успешный (200 OK)
        assert response.status_code == status.HTTP_200_OK

        # Проверяем, что в ответе вернулся один курс (так как мы добавили новый курс)
        assert response.data["count"] == 1  # Поскольку добавлен еще один курс

    def test_retrieve(self, client, user, course):
        """Тест на получение детальной информации о курсе авторизованным пользователем"""
        # Авторизуем пользователя
        client.force_authenticate(user=user)

        # Отправляем GET-запрос на получение подробной информации о конкретном курсе
        response = client.get(self.endpoint + str(course.id) + "/")

        # Проверяем, что ответ успешный (200 OK)
        assert response.status_code == status.HTTP_200_OK

        # Проверяем, что идентификатор курса в ответе совпадает с ожидаемым
        assert str(response.data['id']) == str(course.id)

        # Проверяем, что название курса совпадает с названием курса в базе данных
        assert response.data['title'] == course.title

        # Проверяем, что идентификатор автора курса совпадает с ожидаемым идентификатором автора
        assert response.data['course_author']['public_id'] == str(course.author.public_id)

    def test_create(self, client, user):
        client.force_authenticate(user=user)
        data = {
            "title": "Test Title Course",
            "author": user.public_id.hex
        }

        response = client.post(self.endpoint + 'create/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == data['title']
        assert response.data['course_author']['public_id'] == str(user.public_id)

    def test_edit(self, client, author, course):
        client.force_authenticate(user=author)
        data = {
            "title": "Test title course",
            "author": author.public_id.hex
        }
        response = client.put(self.endpoint + str(course.id) + "/edit/", data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == data['title']

    def test_retrieve_unauthorized(self, client, course):
        """Тест: неавторизованный пользователь НЕ должен иметь доступ к курсу"""
        response = client.get(self.endpoint + str(course.id) + "/")

        # Ожидаем ошибку 401 Unauthorized
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete(self, client, author, course):
        client.force_authenticate(user=author)
        response = client.delete(self.endpoint + str(course.id) + "/delete/")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_list_anonymous(self, client):
        """Тест: неавторизованный пользователь НЕ должен получать список курсов"""
        response = client.get(self.endpoint)

        # Ожидаем ошибку 401 Unauthorized
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_anonymous(self, client, course):
        response = client.get(self.endpoint + str(course.id) + "/")

        # Ожидаем ошибку 401 Unauthorized
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_anonymous(self, client):
        data = {
            "title": "Test Post Body",
            "author": "test_user"
        }
        response = client.post(self.endpoint + 'create/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_edit_anonymous(self, client, course):
        data = {
            "title": "Test Course Body",
            "author": "test_user"
        }
        response = client.get(self.endpoint + str(course.id) + "/edit/", data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_anonymous(self, client, course):
        response = client.delete(self.endpoint + str(course.id) + "/delete/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_edit_not_author(self, client, user, course):
        """Тест: пользователь, не являющийся автором, НЕ должен редактировать курс"""
        client.force_authenticate(user=user)  # Авторизуем пользователя, который не является автором курса
        data = {
            "title": "Updated Course Title",
            "author": user.public_id.hex
        }
        response = client.put(self.endpoint + str(course.id) + "/edit/", data)

        # Проверяем, что редактирование запрещено (403 Forbidden)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_not_author(self, client, user, course):
        """Тест: пользователь, не являющийся автором, НЕ должен удалять курс"""
        client.force_authenticate(user=user)  # Авторизуем пользователя, который не является автором курса
        response = client.delete(self.endpoint + str(course.id) + "/delete/")

        # Проверяем, что удаление запрещено (403 Forbidden)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_enroll(self, client, user, course):
        client.force_authenticate(user=user)
        response = client.post(self.endpoint + str(course.id) + "/enroll/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {"enrolled": True}
        assert course.students.filter(id=user.id).exists()

    def test_unenroll(self, client, user, course):
        client.force_authenticate(user=user)
        course.students.add(user)  # Сначала подписываем пользователя на курс
        response = client.post(self.endpoint + str(course.id) + "/unenroll/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {"unenrolled": True}
        assert not course.students.filter(id=user.id).exists()

    def test_enroll_unauthenticated(self, client, course):
        response = client.post(self.endpoint + str(course.id) + "/enroll/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_unenroll_unauthenticated(self, client, course):
        response = client.post(self.endpoint + str(course.id) + "/unenroll/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_like(self, client, user, course):
        client.force_authenticate(user=user)
        response = client.post(self.endpoint + str(course.id) + "/like/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'liked': True}

        # Получаем объект RegisteredUsers для данного курса и пользователя
        registered_user = RegisteredUsers.objects.get(course=course, user=user)

        # Проверяем, что лайк установлен
        assert registered_user.liked is True
        assert registered_user.disliked is False

    def test_dislike(self, client, user, course):
        client.force_authenticate(user=user)
        response = client.post(self.endpoint + str(course.id) + "/dislike/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'disliked': True}

        # Получаем объект RegisteredUsers для данного курса и пользователя
        registered_user = RegisteredUsers.objects.get(course=course, user=user)

        # Проверяем, что лайк установлен
        assert registered_user.liked is False
        assert registered_user.disliked is True
