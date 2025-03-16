from rest_framework import status

# Импортируем фикстуры для пользователя, автора, урока и курса
from fixtures.user import user, author
from fixtures.course import course
from fixtures.lesson import lesson
from fixtures.flashcard import flashcard1, flashcard2, flashcard3

from flashcard.models import LearnerFlashCard


class TestLessonViewSet:
    # Определяем endpoint для работы с курсами
    endpoint = '/api/v1/lessons/'

    def test_list(self, client, user, lesson):
        """Тест на получение списка уроков авторизованным пользователем"""
        # Авторизуем пользователя как автора
        client.force_authenticate(user=user)

        # Отправляем GET-запрос на список курсов
        response = client.get(self.endpoint)

        # Проверяем, что ответ успешный (200 OK)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve(self, client, user, lesson):
        """Тест на получение детальной информации об уроке авторизованным пользователем"""

        client.force_authenticate(user=user)

        # Отправляем GET-запрос на получение подробной информации о конкретном курсе
        response = client.get(self.endpoint + str(lesson.id) + "/")

        # Проверяем, что ответ успешный (200 OK)
        assert response.status_code == status.HTTP_200_OK

        # Проверяем, что идентификатор курса в ответе совпадает с ожидаемым
        assert str(response.data['id']) == str(lesson.id)

        # Проверяем, что название курса совпадает с названием курса в базе данных
        assert response.data['title'] == lesson.title

        assert response.data['belongs_course'] == 'Test title course'
        assert response.data['title'] == 'Test lesson'

    def test_create(self, client, author, course):
        """Тест на создание урока"""
        client.force_authenticate(user=author)
        data = {
            "title": "Test Title Lesson",
            "course": course.id
        }
        response = client.post(self.endpoint + 'create/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == data['title']
        assert response.data['belongs_course'] == course.title

    def test_create_not_author(self, client, user, course):
        """Тест на создание урока не пользователем"""
        client.force_authenticate(user=user)
        data = {
            "title": "Test Title Lesson",
            "course": course.id
        }
        response = client.post(self.endpoint + 'create/', data)

        # Ожидаем ошибку 403
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_edit(self, client, author, course, lesson):
        """Тест на редактирование урока"""
        client.force_authenticate(user=author)
        data = {
            "title": "Test Title Lesson",
            "course": course.id
        }
        response = client.put(self.endpoint + str(lesson.id) + "/edit/", data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == data['title']

    def test_edit_not_author(self, client, user, course, lesson):
        """Тест на редактирование урока не автором"""
        client.force_authenticate(user=user)
        data = {
            "title": "Test Title Lesson",
            "course": course.id
        }
        response = client.put(self.endpoint + str(lesson.id) + "/edit/", data)

        # Ожидаем ошибку 403
        assert response.status_code == status.HTTP_403_FORBIDDEN

        assert lesson.title != data["title"]

    def test_delete(self, client, author, lesson):
        """Тест на удаление урока"""
        client.force_authenticate(user=author)
        response = client.delete(self.endpoint + str(lesson.id) + "/delete/")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_not_author(self, client, user, lesson):
        """Тест: пользователь, не являющийся автором, НЕ должен удалять урок"""
        client.force_authenticate(user=user)  # Авторизуем пользователя, который не является автором курса
        response = client.delete(self.endpoint + str(lesson.id) + "/delete/")

        # Проверяем, что удаление запрещено (403 Forbidden)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_learner_flashcards(self, client, user, lesson, flashcard1, flashcard2, flashcard3, course):
        """Проверяем получение карточек для изучения урока."""
        client.force_authenticate(user=user)
        course.students.add(user)  # Сначала подписываем пользователя на курс

        # Получаем запись о том, что карточка принадлежит пользователю и не выучена
        LearnerFlashCard.objects.get_or_create(user=user, flashcard=flashcard1, defaults={"learned_word": False})
        LearnerFlashCard.objects.get_or_create(user=user, flashcard=flashcard2, defaults={"learned_word": False})
        LearnerFlashCard.objects.get_or_create(user=user, flashcard=flashcard3, defaults={"learned_word": False})

        # Выполняем запрос
        response = client.get(self.endpoint + str(lesson.id) + "/learn/")

        # Проверяем статус ответа
        assert response.status_code == status.HTTP_200_OK
        # Проверяем, что возвращены все 3 карточки
        assert len(response.data) == 3

    def test_forbidden_access_if_user_not_enrolled(self, client, user, lesson, course):
        """Проверяем, что доступ к карточкам урока запрещен, если пользователь не подписан на курс."""
        client.force_authenticate(user=user)

        response = client.get(self.endpoint + str(lesson.id) + "/learn/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_reset_result_lesson(self, client, user, lesson, flashcard1, flashcard2, flashcard3, course):
        """"""
        client.force_authenticate(user=user)
        course.students.add(user)  # Сначала подписываем пользователя на курс

        # Создаем записи LearnerFlashCard для пользователя
        LearnerFlashCard.objects.get_or_create(user=user, flashcard=flashcard1, defaults={"learned_word": True})
        LearnerFlashCard.objects.get_or_create(user=user, flashcard=flashcard2, defaults={"learned_word": True})
        LearnerFlashCard.objects.get_or_create(user=user, flashcard=flashcard3, defaults={"learned_word": True})

        # Выполняем запрос
        response = client.post(self.endpoint + str(lesson.id) + "/reset/result/")

        # Проверяем статус ответа
        assert response.status_code == status.HTTP_302_FOUND  # Проверяем редирект

        # Получаем все карточки пользователя для конкретного урока
        flashcards = LearnerFlashCard.objects.filter(user=user, flashcard__lesson=lesson)

        # Проверяем, что поле learned_word у каждой карточки равно False
        for flashcard in flashcards:
            assert flashcard.learned_word is False, f"Карточка {flashcard.id} не была сброшена."

    def test_reset_result_lesson_not_enrolled(self, client, user, lesson, course):
        """Проверяем, что доступ к сбросу результатов урока запрещен, если пользователь не подписан на курс."""
        client.force_authenticate(user=user)

        response = client.post(self.endpoint + str(lesson.id) + "/reset/result/")

        # Проверяем статус ответа
        assert response.status_code == status.HTTP_403_FORBIDDEN  # Доступ запрещен

    def test_list_anonymous(self, client):
        """Тест на получение списка уроков неавторизованным пользователем"""
        response = client.get(self.endpoint)

        # Проверяем, что ответ содержит ошибку 401
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_anonymous(self, client, lesson):
        """Тест на получение детальной информации об уроке неавторизованным пользователем"""
        response = client.get(self.endpoint + str(lesson.id) + "/")

        # Проверяем, что ответ содержит ошибку 401
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_anonymous(self, client, course):
        """Тест на создание урока неавторизованным пользователем"""
        data = {
            "title": "Test Title Lesson",
            "course": course.id
        }
        response = client.post(self.endpoint + 'create/', data)

        # Проверяем, что ответ содержит ошибку 401
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_edit_anonymous(self, client, lesson):
        """Тест на редактирование урока неавторизованным пользователем"""
        data = {
            "title": "Test Title Lesson"
        }
        response = client.put(self.endpoint + str(lesson.id) + "/edit/", data)

        # Проверяем, что ответ содержит ошибку 401
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_anonymous(self, client, lesson):
        """Тест на удаление урока неавторизованным пользователем"""
        response = client.delete(self.endpoint + str(lesson.id) + "/delete/")

        # Проверяем, что ответ содержит ошибку 401
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_learner_flashcards_unauthenticated(self, client, lesson):
        """Тест на получение карточек урока неавторизованным пользователем"""
        response = client.get(self.endpoint + str(lesson.id) + "/learn/")

        # Проверяем, что ответ содержит ошибку 401
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_reset_result_lesson_unauthenticated(self, client, lesson):
        """Тест на сброс результатов урока неавторизованным пользователем"""
        response = client.post(self.endpoint + str(lesson.id) + "/reset/result/")

        # Проверяем, что ответ содержит ошибку 401
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
